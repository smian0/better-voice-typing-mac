# Voice Typing Assistant

A lightweight Python Windows desktop app alternative to Windows Voice Typing (Win+H).

## Overview

The app works as follows:
- Press Caps Lock to begin recording your voice (without activating Caps Lock)
- A small red indicator appears in the top-right corner showing "🎤 Recording"
- Press Caps Lock again to stop recording and process the audio
- The audio is sent to OpenAI Whisper for transcription
- The transcribed text is cleaned (if enabled) and inserted at the cursor location
- Settings can be accessed via the system tray icon

## Features

### Keyboard Controls
- **Toggle Recording**: Caps Lock (normal Caps Lock functionality still available with Ctrl+Caps Lock)
- **Cancel Recording**: Click the recording indicator

### UI Feedback
- Minimal floating indicator in top-right corner
- Pulsing red animation during recording
- Clickable to cancel recording

### System Tray
- Accessible settings menu
- Clean transcription toggle
- Easy exit option

### Settings
- Clean Transcription: Enable/disable text cleanup
- Continuous Capture (planned feature): Record audio until the user stops it, send it all at once to OpenAi Whisper and then Anthropic Claude Haiku for cleaning up
- Smart Capture (planned feature): Record audio in 1-2 minute chunks (looking for ~1 second of silence to trigger the chunk) send each chunk to OpenAi Whisper in the background and collect the results, then send the whole lot to Anthropic Claude Haiku for cleaning up

## Technical Details
- Built with Python using tkinter for UI
- Uses pynput for keyboard handling
- OpenAI Whisper API for transcription
- Supports Windows OS

## Dependencies
- python-dotenv: Environment variables
- pynput: Keyboard shortcuts
- sounddevice & soundfile: Audio recording
- openai: Whisper API integration
- anthropic: Text cleanup (planned)
- pyautogui: Text insertion
- pystray: System tray functionality
- Pillow: Icon handling

## TODO
- Select mic via taskbar icon (see https://github.com/bsnjoy/voice-typing/blob/main/select_mic.py)
- Restore clipboard after text insertion (see https://github.com/bsnjoy/voice-typing/blob/654698d262c52d11c7f5e18f739483ed2cea6838/voice_typing.py#L151)
- Implement Smart Capture mode
- Implement Continuous Capture mode
