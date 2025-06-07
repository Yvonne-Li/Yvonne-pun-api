```/api/chat``` - Uses OpenAI to generate custom puns \
```/api/puns``` - Returns pre-defined puns from a database

TRY IT OUT
```Bash
curl -X POST https://yvonne-pun-api.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me puns about cats"}'
```
```bash
tree -I 'node_modules|.git|dist|build' > project_structure.txt
```