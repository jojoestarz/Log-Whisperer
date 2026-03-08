# Gemini Integration Setup

The Log Whisperer now supports Google Gemini as an alternative to Anthropic Claude.

## Quick Setup

1. **Get your Gemini API key**
   - Visit: https://aistudio.google.com/app/apikey
   - Create a new API key (free tier available)

2. **Update your .env file**
   ```bash
   # Set the LLM provider
   LLM_PROVIDER=gemini
   
   # Add your Gemini API key
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Install dependencies**
   ```bash
   pip install google-generativeai
   # Or install all requirements:
   pip install -r requirements.txt
   ```

4. **Test the integration**
   ```bash
   python test_gemini.py
   ```

## Model Mapping

The system automatically maps Claude model names to Gemini equivalents:

| Claude Model | Gemini Model |
|-------------|--------------|
| claude-sonnet-4-20250514 | gemini-1.5-pro |
| claude-3-5-sonnet-20241022 | gemini-1.5-pro |
| claude-3-sonnet-20240229 | gemini-1.5-flash |

## Switching Between Providers

To switch back to Anthropic, just update your .env:

```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_key
```

## Cost Comparison

**Gemini 1.5 Pro (Free Tier)**
- 50 requests per day
- Rate limit: 2 requests per minute

**Gemini 1.5 Flash (Free Tier)**
- 1,500 requests per day
- Rate limit: 15 requests per minute

**Anthropic Claude**
- Pay-as-you-go pricing
- No free tier

## Troubleshooting

If you get authentication errors:
1. Verify your API key is correct in .env
2. Check you haven't exceeded rate limits
3. Ensure `google-generativeai` package is installed

Run the test script for detailed diagnostics:
```bash
python test_gemini.py
```
