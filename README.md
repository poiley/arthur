# Arthur

Homebrew personal assistant

Voice powered by IBM watson

## Setup

Install pips

```
pip install -r requirements.txt

```

Create keyfile `keys.json`

```
{
	"stt_username": "",
	"stt_password": "",
	"tts_username": "",
	"tts_password": "",
	"voice": "en-US_AllisonVoice"
}
```

## Plugins

Add pluginst to arthur in just a few lines! To run function `func()`:

```
assistant = arthur.Arthur()

my_plugin = plugin.plugin("My Plugin Name", func, "Phrase that triggers plugin") 
	
assistant.add_plugin(my_plugin)

```