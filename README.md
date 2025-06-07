```/api/chat``` - Uses OpenAI to generate custom puns \
```/api/puns``` - Returns pre-defined puns from a database

TRY IT OUT
```Bash
curl -X POST https://your-vercel-domain.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me puns about cats"}'
```