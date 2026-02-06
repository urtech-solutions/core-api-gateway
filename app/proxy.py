import httpx
from fastapi import Request, Response

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "host",
}


def _filtered_headers(headers: httpx.Headers | dict[str, str]) -> dict[str, str]:
    return {k: v for k, v in headers.items() if k.lower() not in HOP_BY_HOP_HEADERS}


async def forward_request(
    request: Request, upstream_base_url: str, path_suffix: str = ""
) -> Response:
    upstream_path = path_suffix or ""
    upstream_url = f"{upstream_base_url.rstrip('/')}{upstream_path}"

    body = await request.body()
    headers = _filtered_headers(request.headers)

    async with httpx.AsyncClient(timeout=30.0) as client:
        upstream_response = await client.request(
            method=request.method,
            url=upstream_url,
            params=request.query_params,
            headers=headers,
            content=body,
        )

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=_filtered_headers(upstream_response.headers),
        media_type=upstream_response.headers.get("content-type"),
    )
