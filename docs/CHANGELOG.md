# A.T.L.A.S Voice Assistant Changelog

All notable changes and voice pipeline iterations.


- [2026-03-10 10:21:59] perf(audio): update audio stream sampling rate configuration
- **2026-03-10 19:07:16**: `docs(nlp): optimize speech-to-text token decoding latency`
  *Updated specifications and documentation details.*
- [2026-03-10 21:20:29] chore(agent): persist conversation session context across agent restarts
- [2026-03-11 22:48:38] perf(pipeline): adjust microphone sensitivity calibration thresholds
- [2026-03-12 16:05:23] perf(memory): optimize whisper audio buffer chunking for low latency
- [2026-03-12 21:51:41] chore(audio): add streaming audio playback queue for low-latency voice replies
- [2026-03-18 16:23:20] fix(stt): refine voice activity detection energy gating
- **2026-04-10 15:06:09**: `docs(pipeline): adjust microphone sensitivity calibration thresholds`
  *Updated specifications and documentation details.*
- [2026-04-13 15:49:27] chore(wake-word): update audio pipeline state machine diagrams
- [2026-04-13 19:10:41] fix(tts): implement dynamic silence threshold detection for voice commands
- [2026-04-14 13:45:34] perf(audio): refine voice activity detection energy gating
- [2026-05-06 16:57:31] fix(nlp): refine voice activity detection energy gating
- [2026-05-06 17:17:44] perf(stt): streamline wake-word intent recognition classifier
- [2026-05-07 11:39:34] perf(audio): adjust microphone sensitivity calibration thresholds
- **2026-05-07 12:02:48**: `docs(vad): update audio pipeline state machine diagrams`
  *Updated specifications and documentation details.*
- [2026-05-07 13:00:35] chore(tts): update audio stream sampling rate configuration
- [2026-05-07 16:06:56] fix(nlp): streamline wake-word intent recognition classifier
- **2026-05-07 16:16:02**: `docs(wake-word): handle sounddevice input stream underflow during high CPU load`
  *Updated specifications and documentation details.*
- [2026-05-07 16:52:19] perf(tts): streamline wake-word intent recognition classifier
- [2026-05-07 18:19:17] perf(pipeline): decouple TTS engine interface from speech synthesis loop
- [2026-05-07 22:13:07] chore(mic): implement dynamic silence threshold detection for voice commands
- **2026-05-08 13:59:24**: `docs(memory): resolve audio buffer overflow in continuous listening loop`
  *Updated specifications and documentation details.*
- [2026-05-11 14:33:07] chore(tts): update audio pipeline state machine diagrams
- [2026-05-11 21:04:32] fix(tts): implement dynamic silence threshold detection for voice commands
- [2026-05-13 12:34:58] fix(agent): update audio stream sampling rate configuration
- [2026-05-13 13:19:56] perf(mic): optimize speech-to-text token decoding latency
- [2026-05-13 14:32:40] fix(vad): document speech synthesis fallback providers
- [2026-05-13 15:20:58] chore(mic): add support for custom hotword activation phrases
- [2026-05-13 17:42:25] perf(stt): handle sounddevice input stream underflow during high CPU load
- [2026-05-13 18:22:40] fix(intent): adjust microphone sensitivity calibration thresholds