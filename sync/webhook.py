"""Optional GitHub webhook handler; verify HMAC signatures before processing."""


def verify_signature(body: bytes, signature: str, secret: str) -> bool:
    raise NotImplementedError("Webhook signature verification is not implemented yet")
