# Changelog

## [1.1.0] - 2026-06-19

### Changed
- OCR now processes pages one-by-one instead of loading all page images into memory at once, reducing peak RAM per request from ~550MB to ~11MB.
- Merged text-layer detection into `_extract_text` to eliminate one redundant full PDF parse per request.
- `PdfReader` now uses `with` statement for guaranteed cleanup.
- Removed unused `BytesIO` import and redundant `del images`.
- Workflow trigger changed from `push` on `main` to `release` published, with Docker tags derived from semver release tag.

### Added
- `lang` query parameter to `POST /parse` endpoint (e.g., `?lang=por`, `?lang=spa`), defaults to `"eng"`.
- `CHANGELOG.md`.

## [1.0.2] - 2025-03-30

### Changed
- Bumped `python-multipart` from 0.0.27 to 0.0.31.
- Bumped `pypdf` from 6.12.0 to 6.13.3.

## [1.0.1] - 2025-03-21

### Changed
- Bumped `pypdf` from 5.1.0 to 6.12.0.
- Bumped `python-multipart` from 0.0.19 to 0.0.27.
- Bumped `pillow` from 11.1.0 to 12.2.0.

## [1.0.0] - 2025-03-18

### Added
- Initial release of PDF Parser service.
- `POST /parse` endpoint for PDF text extraction and OCR.
- `GET /health` endpoint for health checks.
- Text extraction via `pypdf`.
- OCR fallback via `pdf2image` + `pytesseract`.
- Docker image with multi-stage build and non-root user.
- CORS middleware with configurable origins.
- Concurrency limiting via semaphore (default 4).
- File validation (extension, magic bytes, size cap).
- GitHub Actions CI/CD for Docker Hub publishing on release.
