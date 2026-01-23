

PART 1: Authenticate Cloudflare Tunnel

```
docker run -it --rm cloudflare/cloudflared:latest tunnel login
docker run -it --rm cloudflare/cloudflared:latest tunnel create recipe-api
```

PART 2: Create a tunnel
```
docker run -it --rm cloudflare/cloudflared:latest tunnel create recipe-api
```
You'll get Tunnel ID
credentials.json


PART 3: Docker Compose

Create dockerfile
Create docker-compose.yaml
Create cloudflared/config.yml



PART 4:  Create DNS route (no A records)
This replaces Namecheap A records completely.
```
docker run -it --rm cloudflare/cloudflared:latest tunnel route dns recipe-api api.yourdomain.com
```
Cloudflare now:
Creates a CNAME behind the scenes
Routes traffic through the tunnel
Automatically serves HTTPS


PART 5: Run everything
```
docker compose up -d --build
```


Check logs
```
docker logs cloudflared
docker logs recipe_api
```


Test:
```
https://api.yourdomain.com/health
```



TODO:
[x] Get API token for personal use and add support to it to backend
[] n8n sort out how to extract the recipe with AI
[x] add postgresql to the backend
[x] create frontend that shows all recipes
[x] serve images using Caddy


NEXT STEPS:

```
docker run -it --rm cloudflare/cloudflared:latest tunnel route dns recipe-app recipe.domain.com
```


use caddy to change the flask API to use /api in recipe.
```
tunnel: 916b4f0b-433b-4ea4-b053-be4fc2277d14
credentials-file: /etc/cloudflared/credentials.json

ingress:
  - hostname: recipe.lucientran.com
    service: http://caddy:80


  - service: http_status:404
```

In root directory:
```
docker-compose up --build
```

