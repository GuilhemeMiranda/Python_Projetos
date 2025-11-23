# 🚀 Quick Start Guide

Get up and running with the Vehicle Maintenance API in 5 minutes!

## ⚡ Fast Setup

### Option 1: Using Make (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/GuilhemeMiranda/Python_Projetos.git
cd Python_Projetos

# 2. Setup everything
make setup

# 3. Run the application
make run
```

Visit: http://localhost:8000/docs

### Option 2: Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/GuilhemeMiranda/Python_Projetos.git
cd Python_Projetos

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

### Option 3: Using Docker

```bash
# 1. Clone the repository
git clone https://github.com/GuilhemeMiranda/Python_Projetos.git
cd Python_Projetos

# 2. Start with Docker Compose
docker-compose up
```

Visit: http://localhost:8000/docs

## 🎯 First API Call

```bash
# Test the API
curl http://localhost:8000/

# Expected response:
# {"mensagem":"Bem-vindo à API de Manutenção Veicular 🚗"}
```

## 📝 Create Your First User

```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@exemplo.com",
    "senha": "senha123"
  }'
```

## 🚗 Register a Vehicle

```bash
curl -X POST "http://localhost:8000/veiculos/" \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC-1234",
    "modelo": "Civic",
    "marca": "Honda",
    "ano": 2020,
    "km_atual": 15000,
    "usuario_id": 1
  }'
```

## 🧪 Run Tests

```bash
# Using make
make test

# Or directly with pytest
pytest tests/ -v
```

## 📚 Useful Commands

```bash
# View all available commands
make help

# Format code
make format

# Run linters
make lint

# View logs
docker-compose logs -f

# Stop Docker containers
docker-compose down
```

## 🔗 Important Links

- **API Documentation:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Full README:** [README.md](README.md)
- **API Guide:** [docs/API_GUIDE.md](docs/API_GUIDE.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Git Commands:** [docs/GIT_COMMANDS.md](docs/GIT_COMMANDS.md)
- **Security:** [docs/SECURITY.md](docs/SECURITY.md)

## ❓ Need Help?

1. Check the [README.md](README.md) for detailed documentation
2. View [API_GUIDE.md](docs/API_GUIDE.md) for endpoint examples
3. Open an [issue](https://github.com/GuilhemeMiranda/Python_Projetos/issues)

## 🎓 Next Steps

1. Explore the interactive API docs at http://localhost:8000/docs
2. Read the [CONTRIBUTING.md](CONTRIBUTING.md) guide
3. Check out the test examples in `tests/`
4. Review security best practices in [docs/SECURITY.md](docs/SECURITY.md)

---

**Happy coding! 🎉**
