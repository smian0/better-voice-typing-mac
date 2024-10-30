I want to build a light weight Python windows desktop app for myself as an alternative to Windows Voice Typing (activated by Win H)

## Overview

It would work like this:
- user presses keyboard shortcut to begin recording the users voice
- there is no UI, but where the user had the cursor a "listening..." is temporarily entered with the dots edited to show active listening, eg. "." then "..", "...", "..", "."
- the listening will continue until the user presses the keyboard shortcut again to stop the recording and send it for processing
- the audio is sent to OpenAi Whisper, then the text is processed by Anthropic Claude Haiku to clean it up, before being inserted at the current cursor location
- the user can change some settings and options via the taskbar icon

## Detailed Requirements

Keyboard Shortcut Activation
Start Recording: Press a predefined shortcut to begin voice capture.
Stop Recording: Press the same shortcut to end recording and initiate processing.

Minimal UI Feedback
In-line Indicator: Insert "listening..." at the current cursor location.
Animation: Update the dots (e.g., ".", "..", "...") to show active listening.
Cleanup: Remove or replace the indicator with transcribed text after processing.

Voice Recording
(default) Continuous Capture: Record audio until the user stops it, send it all at once to OpenAi Whisper and then Anthropic Claude Haiku for cleaning up
(alternative, later) Smart Capture: Record audio in 1-2 minute chunks (looking for ~1 second of silence to trigger the chunk) send each chunk to OpenAi Whisper in the background and collect the results, then send the whole lot to Anthropic Claude Haiku for cleaning up
Format Compatibility: Save audio in .mp4 format, which is compatible with OpenAi Whisper

Speech Recognition Processing
Error Handling: Manage failures gracefully and inform the user, likely by inserting the (shortned) error message into the text.

Settings and Options
For now, just choice of Continuous Capture mode, Smart Capture mode and exit
Have icon change to one that indicates recording