

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


