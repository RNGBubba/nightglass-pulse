# Nightglass Pulse — original instrumental loop

## Offer
A ready-to-use 20-second stereo WAV loop plus a small, dependency-free Python renderer for creators who need an original neon-night music bed for a short video, podcast bumper, stream interstitial, or prototype. The composition is instrumental and contains no lyrics, samples, covers, or borrowed melody.

## Included artifact
- `nightglass-pulse.wav` — 20.000 seconds, stereo, 44.1 kHz, 16-bit PCM.
- `generate_loop.py` — deterministic renderer for the WAV, using only the Python standard library.
- `README.md` — usage and originality notes.

The loop is in D dorian at 120 BPM (10 bars of 4/4). It uses an original syncopated pluck motif, sustained chord voicings, synthesized bass, kick, snare/noise backbeat, and hats. The final 80 ms are crossfaded against the opening to reduce an audible seam when repeated.

## License / use
The repository is a transparent original-work release. Users may use and adapt the audio in their own projects, including commercial projects, while keeping this attribution: “Nightglass Pulse by RNGBubba.” Do not present the composition as an existing artist's recording or as a cover.

## Suggested price and 30-day path
- Suggested one-time price: $9 for the WAV + renderer + attribution-free commercial-use permission, if later listed on an already-authenticated storefront.
- 30-day path: publish the public repository tonight; add a storefront listing only when an approved, already-authenticated payment rail is available; post the repository link in relevant creator communities without spam; release one additional original loop as a separate repository if this receives organic interest.
- Human click required: a storefront owner must approve the listing and any payment setup. This run does not spend money or create a storefront listing.

## Verification
- `python -m py_compile generate_loop.py`
- `python generate_loop.py`
- `ffprobe -v error -show_entries format=duration:stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 nightglass-pulse.wav`

Observed output: a 20.000-second, stereo, 44,100 Hz, `pcm_s16le` WAV was generated successfully.

## Provenance and limitations
This is newly written synthesis code and musical material created for this repository. It is not a transcription or remix. No external samples, copyrighted lyrics, or existing-song cover material are included. The renderer intentionally favors a compact, clean synthetic sound rather than claiming studio mastering.

## Repository
A new public GitHub repository is intended for this artifact. The final URL is recorded below after publication.

GitHub URL: https://github.com/RNGBubba/nightglass-pulse
