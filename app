import os, base64, tempfile
from datetime import datetime, timezone
import soundfile as sf
import boto3
import numpy as np
import torch
import torchaudio
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from speechbrain.pretrained import EncoderClassifier

# AWS clients
s3 = boto3.client("s3")
ddb = boto3.client("dynamodb")

TABLE = "speaker_embeddings"
THRESHOLD = 0.75

# Load model ONCE
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb"
)

app = FastAPI()

class EnrollReq(BaseModel):
    speaker_id: str
    bucket: str
    key: str

class VerifyReq(BaseModel):
    speaker_id: str
    bucket: str
    key: str

def download_audio(bucket, key):
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    s3.download_file(bucket, key, path)
    return path

def load_audio(path):
    data, sr = sf.read(path, dtype="float32")

    # Convert to torch tensor
    sig = torch.from_numpy(data)

    # If stereo → mono
    if sig.ndim > 1:
        sig = sig.mean(dim=1)

    sig = sig.unsqueeze(0)  # [1, T]

    # Resample if needed
    if sr != 16000:
        sig = torchaudio.functional.resample(sig, sr, 16000)
    return sig
def embed(sig):
    with torch.no_grad():
        emb = classifier.encode_batch(sig).squeeze()
    emb = emb / torch.norm(emb, p=2)
    return emb.cpu()

def to_b64(emb):
    arr = emb.numpy().astype(np.float32)
    return base64.b64encode(arr.tobytes()).decode()

def from_b64(b64):
    arr = np.frombuffer(base64.b64decode(b64), dtype=np.float32)
    t = torch.from_numpy(arr)
    return t / torch.norm(t, p=2)

@app.post("/enroll")
def enroll(req: EnrollReq):
    path = download_audio(req.bucket, req.key)
    try:
        sig = load_audio(path)
        emb = embed(sig)
        b64 = to_b64(emb)
        ddb.put_item(
            TableName=TABLE,
            Item={
                "speaker_id": {"S": req.speaker_id},
                "embedding": {"S": b64},
                "updated_at": {"S": datetime.now(timezone.utc).isoformat()}
            }
        )
        return {"status": "ENROLLED"}
    finally:
        os.remove(path)

@app.post("/verify")
def verify(req: VerifyReq):
    resp = ddb.get_item(
        TableName=TABLE,
        Key={"speaker_id": {"S": req.speaker_id}}
    )
    if "Item" not in resp:
        raise HTTPException(404, "Speaker not enrolled")

    enrolled = from_b64(resp["Item"]["embedding"]["S"])
    path = download_audio(req.bucket, req.key)
    try:
        sig = load_audio(path)
        probe = embed(sig)
        score = float(F.cosine_similarity(enrolled, probe, dim=0))
        return {
            "score": score,
            "match": score >= THRESHOLD
        }
    finally:
        os.remove(path)

@app.get("/health")
def health():
    return {"ok": True}
