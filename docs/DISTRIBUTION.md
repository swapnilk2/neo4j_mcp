# Distribution and Packaging Guide

This guide provides comprehensive instructions for packaging, distributing, and deploying the Neo4j MCP server for end users across different platforms and environments.

## 📦 Package Structure

### Complete Package Layout
```
neo4j_mcp/
├── src/neo4j_mcp/           # Main package source
│   ├── __init__.py
│   ├── server.py            # MCP server implementation
│   ├── config.py            # Configuration management
│   ├── connection.py        # Neo4j connection handling
│   └── tools/               # MCP tools
│       ├── __init__.py
│       ├── schema.py        # Schema introspection
│       ├── read_query.py    # Read operations
│       ├── write_query.py   # Write operations
│       └── config_tool.py   # Runtime configuration
├── docs/                    # Documentation
│   ├── PLATFORM_SETUP.md
│   ├── CLAUDE_CODE_INTEGRATION.md
│   ├── TROUBLESHOOTING.md
│   ├── EXAMPLES.md
│   └── DISTRIBUTION.md      # This file
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_connection.py
│   ├── test_tools/
│   └── fixtures/
├── examples/                # Example configurations
│   ├── claude_configs/
│   ├── sample_queries/
│   └── deployment_scripts/
├── scripts/                 # Utility scripts
│   ├── setup_dev.py
│   ├── test_connection.py
│   └── package_build.py
├── requirements.txt         # Python dependencies
├── setup.py                # Package setup
├── pyproject.toml          # Modern Python packaging
├── MANIFEST.in             # Package manifest
├── README.md               # Main documentation
├── LICENSE                 # MIT License
├── CHANGELOG.md            # Version history
└── .github/                # GitHub workflows
    └── workflows/
        ├── test.yml
        ├── build.yml
        └── release.yml
```

---

## 🔧 Building and Packaging

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-username/neo4j_mcp.git
cd neo4j_mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Package Building

#### Using setuptools (Traditional)

```bash
# Install build dependencies
pip install build twine wheel

# Build source distribution
python setup.py sdist

# Build wheel distribution
python setup.py bdist_wheel

# Build both
python -m build

# Verify package contents
tar -tzf dist/neo4j_mcp-*.tar.gz
unzip -l dist/neo4j_mcp-*.whl
```

#### Using pyproject.toml (Modern)

```bash
# Install modern build tools
pip install build

# Build package
python -m build

# Check package
python -m twine check dist/*
```

#### Example setup.py

```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="neo4j-mcp",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Neo4j Model Context Protocol server with cross-platform support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/neo4j_mcp",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/neo4j_mcp/issues",
        "Documentation": "https://your-username.github.io/neo4j_mcp",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "neo4j-mcp-server=neo4j_mcp.server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "neo4j_mcp": ["py.typed"],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
            "pre-commit>=2.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.15",
        ],
    },
)
```

#### Example pyproject.toml

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm"]
build-backend = "setuptools.build_meta"

[project]
name = "neo4j-mcp"
dynamic = ["version"]
description = "Neo4j Model Context Protocol server with cross-platform support"
readme = "README.md"
license = {file = "LICENSE"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
requires-python = ">=3.8"
dependencies = [
    "mcp>=0.5.0",
    "neo4j>=5.0.0",
    "rich>=10.0.0",
    "python-dotenv>=0.19.0",
    "pydantic>=1.8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=6.0",
    "pytest-cov>=2.0",
    "black>=21.0",
    "flake8>=3.8",
    "mypy>=0.812",
    "pre-commit>=2.0",
]
docs = [
    "sphinx>=4.0",
    "sphinx-rtd-theme>=1.0",
    "myst-parser>=0.15",
]

[project.urls]
Homepage = "https://github.com/your-username/neo4j_mcp"
Documentation = "https://your-username.github.io/neo4j_mcp"
Repository = "https://github.com/your-username/neo4j_mcp.git"
Issues = "https://github.com/your-username/neo4j_mcp/issues"

[project.scripts]
neo4j-mcp-server = "neo4j_mcp.server:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
neo4j_mcp = ["py.typed"]

[tool.setuptools_scm]
write_to = "src/neo4j_mcp/_version.py"
```

---

## 🚀 Distribution Methods

### 1. PyPI Distribution

#### Initial Setup
```bash
# Create PyPI account at https://pypi.org
# Install twine
pip install twine

# Create ~/.pypirc
[distutils]
index-servers = pypi

[pypi]
username = __token__
password = pypi-your-api-token-here
```

#### Publishing Process
```bash
# Build package
python -m build

# Upload to test PyPI first
python -m twine upload --repository testpypi dist/*

# Test installation from test PyPI
pip install --index-url https://test.pypi.org/simple/ neo4j-mcp

# Upload to production PyPI
python -m twine upload dist/*

# Verify installation
pip install neo4j-mcp
```

### 2. GitHub Releases

#### Automated Release with GitHub Actions

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine

    - name: Build package
      run: python -m build

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*

    - name: Create GitHub Release
      uses: softprops/action-gh-release@v1
      with:
        files: dist/*
        generate_release_notes: true
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### Manual Release Process
```bash
# Tag version
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Create release assets
python -m build
zip -r neo4j-mcp-1.0.0.zip src/ docs/ examples/ requirements.txt setup.py README.md LICENSE

# Upload via GitHub UI or gh CLI
gh release create v1.0.0 dist/* neo4j-mcp-1.0.0.zip --title "Neo4j MCP v1.0.0" --notes-file RELEASE_NOTES.md
```

### 3. Docker Distribution

#### Dockerfile
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY requirements.txt .
COPY setup.py .
COPY src/ src/
COPY README.md .
COPY LICENSE .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN groupadd -r neo4j-mcp && useradd -r -g neo4j-mcp neo4j-mcp
USER neo4j-mcp

# Expose port (if needed)
EXPOSE 8000

# Set default command
CMD ["python", "-m", "neo4j_mcp.server"]
```

#### Docker Compose for Development
```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:latest
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      - NEO4J_AUTH=neo4j/password
    volumes:
      - neo4j-data:/data

  neo4j-mcp:
    build: .
    depends_on:
      - neo4j
    environment:
      - NEO4J_URI=neo4j://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password
    stdin_open: true
    tty: true

volumes:
  neo4j-data:
```

#### Building and Publishing Docker Images
```bash
# Build image
docker build -t neo4j-mcp:1.0.0 .
docker tag neo4j-mcp:1.0.0 neo4j-mcp:latest

# Push to Docker Hub
docker tag neo4j-mcp:1.0.0 your-username/neo4j-mcp:1.0.0
docker push your-username/neo4j-mcp:1.0.0
docker push your-username/neo4j-mcp:latest

# GitHub Container Registry
docker tag neo4j-mcp:1.0.0 ghcr.io/your-username/neo4j-mcp:1.0.0
docker push ghcr.io/your-username/neo4j-mcp:1.0.0
```

### 4. Conda Distribution

#### meta.yaml for conda-forge
```yaml
{% set name = "neo4j-mcp" %}
{% set version = "1.0.0" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.io/packages/source/{{ name[0] }}/{{ name }}/neo4j-mcp-{{ version }}.tar.gz
  sha256: your-package-sha256-here

build:
  noarch: python
  script: {{ PYTHON }} -m pip install . -vv
  number: 0
  entry_points:
    - neo4j-mcp-server = neo4j_mcp.server:main

requirements:
  host:
    - python >=3.8
    - pip
  run:
    - python >=3.8
    - mcp >=0.5.0
    - neo4j >=5.0.0
    - rich >=10.0.0
    - python-dotenv >=0.19.0
    - pydantic >=1.8.0

test:
  imports:
    - neo4j_mcp
  commands:
    - neo4j-mcp-server --help

about:
  home: https://github.com/your-username/neo4j_mcp
  license: MIT
  license_file: LICENSE
  summary: Neo4j Model Context Protocol server with cross-platform support
  description: |
    A comprehensive Model Context Protocol (MCP) server for Neo4j database
    integration with cross-platform support and zero APOC dependencies.
  doc_url: https://your-username.github.io/neo4j_mcp
  dev_url: https://github.com/your-username/neo4j_mcp

extra:
  recipe-maintainers:
    - your-username
```

---

## 📋 Platform-Specific Packaging

### Windows Packaging

#### Using cx_Freeze
```python
# setup_freeze.py
from cx_Freeze import setup, Executable
import sys

# Dependencies are automatically detected, but it may need fine tuning.
build_options = {
    'packages': ['neo4j_mcp', 'neo4j', 'mcp', 'rich'],
    'excludes': ['tkinter'],
    'include_files': ['docs/', 'examples/']
}

base = 'Console'

executables = [
    Executable('src/neo4j_mcp/server.py', base=base, target_name='neo4j-mcp-server.exe')
]

setup(
    name='Neo4j MCP Server',
    version='1.0.0',
    description='Neo4j Model Context Protocol server',
    options={'build_exe': build_options},
    executables=executables
)
```

#### Using PyInstaller
```bash
# Install PyInstaller
pip install pyinstaller

# Create standalone executable
pyinstaller --onefile \
    --add-data "docs:docs" \
    --add-data "examples:examples" \
    --name neo4j-mcp-server \
    src/neo4j_mcp/server.py

# Create installer with NSIS (optional)
makensis installer.nsi
```

#### Windows Installer (NSIS Script)
```nsis
; installer.nsi
!include "MUI2.nsh"

Name "Neo4j MCP Server"
OutFile "Neo4j_MCP_Setup.exe"
InstallDir "$PROGRAMFILES\Neo4j MCP Server"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File /r "dist\neo4j-mcp-server\*"
    CreateShortCut "$DESKTOP\Neo4j MCP Server.lnk" "$INSTDIR\neo4j-mcp-server.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Neo4jMCP" "DisplayName" "Neo4j MCP Server"
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd
```

### macOS Packaging

#### Using py2app
```python
# setup_mac.py
from setuptools import setup

APP = ['src/neo4j_mcp/server.py']
DATA_FILES = [
    ('docs', ['docs/']),
    ('examples', ['examples/'])
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['neo4j_mcp', 'neo4j', 'mcp', 'rich'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

#### Creating DMG
```bash
# Build app
python setup_mac.py py2app

# Create DMG
hdiutil create -volname "Neo4j MCP Server" \
    -srcfolder dist/server.app \
    -ov -format UDZO \
    Neo4j_MCP_Installer.dmg
```

### Linux Packaging

#### DEB Package (Debian/Ubuntu)
```bash
# Create package structure
mkdir -p neo4j-mcp_1.0.0/DEBIAN
mkdir -p neo4j-mcp_1.0.0/usr/local/bin
mkdir -p neo4j-mcp_1.0.0/usr/share/doc/neo4j-mcp

# Control file
cat > neo4j-mcp_1.0.0/DEBIAN/control << EOF
Package: neo4j-mcp
Version: 1.0.0
Section: database
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-pip
Maintainer: Your Name <your.email@example.com>
Description: Neo4j Model Context Protocol server
 A comprehensive MCP server for Neo4j database integration
 with cross-platform support and zero APOC dependencies.
EOF

# Install script
cat > neo4j-mcp_1.0.0/DEBIAN/postinst << EOF
#!/bin/bash
pip3 install neo4j-mcp
EOF

# Build package
dpkg-deb --build neo4j-mcp_1.0.0
```

#### RPM Package (Red Hat/CentOS/Fedora)
```spec
# neo4j-mcp.spec
Name:           neo4j-mcp
Version:        1.0.0
Release:        1%{?dist}
Summary:        Neo4j Model Context Protocol server
License:        MIT
URL:            https://github.com/your-username/neo4j_mcp
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
Requires:       python3 >= 3.8

%description
A comprehensive MCP server for Neo4j database integration
with cross-platform support and zero APOC dependencies.

%prep
%setup -q

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --root %{buildroot}

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/*
%{_bindir}/neo4j-mcp-server

%changelog
* Mon Jan 15 2024 Your Name <your.email@example.com> - 1.0.0-1
- Initial package
```

---

## 🔄 Continuous Integration and Deployment

### GitHub Actions Workflow

#### Complete CI/CD Pipeline
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, '3.10', 3.11, 3.12]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        pip install -e .

    - name: Run tests
      run: |
        pytest tests/ -v --cov=neo4j_mcp --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Build package
      run: |
        pip install build
        python -m build

    - name: Store artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  publish:
    if: github.event_name == 'release'
    needs: [test, build]
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Download artifacts
      uses: actions/download-artifact@v3
      with:
        name: dist
        path: dist/

    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        pip install twine
        twine upload dist/*
```

### Quality Assurance

#### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
    -   id: flake8

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
    -   id: mypy
```

#### Test Configuration
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --disable-warnings
    --cov=neo4j_mcp
    --cov-report=term-missing
    --cov-report=html
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

---

## 🎯 Deployment Strategies

### Enterprise Deployment

#### Kubernetes Deployment
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neo4j-mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: neo4j-mcp-server
  template:
    metadata:
      labels:
        app: neo4j-mcp-server
    spec:
      containers:
      - name: neo4j-mcp
        image: your-username/neo4j-mcp:1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: NEO4J_URI
          valueFrom:
            secretKeyRef:
              name: neo4j-credentials
              key: uri
        - name: NEO4J_USER
          valueFrom:
            secretKeyRef:
              name: neo4j-credentials
              key: username
        - name: NEO4J_PASSWORD
          valueFrom:
            secretKeyRef:
              name: neo4j-credentials
              key: password
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: neo4j-mcp-service
spec:
  selector:
    app: neo4j-mcp-server
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

#### Docker Swarm
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  neo4j-mcp:
    image: your-username/neo4j-mcp:1.0.0
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    environment:
      - NEO4J_URI_FILE=/run/secrets/neo4j_uri
      - NEO4J_USER_FILE=/run/secrets/neo4j_user
      - NEO4J_PASSWORD_FILE=/run/secrets/neo4j_password
    secrets:
      - neo4j_uri
      - neo4j_user
      - neo4j_password
    networks:
      - neo4j-network

secrets:
  neo4j_uri:
    external: true
  neo4j_user:
    external: true
  neo4j_password:
    external: true

networks:
  neo4j-network:
    driver: overlay
```

### Cloud Deployment

#### AWS Lambda
```python
# lambda_handler.py
import json
from neo4j_mcp.server import run_server

def lambda_handler(event, context):
    # Initialize MCP server for Lambda
    response = run_server(event)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
```

#### Google Cloud Functions
```python
# main.py
import functions_framework
from neo4j_mcp.server import run_server

@functions_framework.http
def neo4j_mcp_handler(request):
    return run_server(request)
```

#### Azure Functions
```python
# function_app.py
import azure.functions as func
from neo4j_mcp.server import run_server

app = func.FunctionApp()

@app.route(route="neo4j_mcp")
def neo4j_mcp_handler(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        run_server(req),
        status_code=200
    )
```

---

## 📊 Distribution Analytics

### Package Download Tracking

#### PyPI Statistics
```python
# scripts/download_stats.py
import requests
import json

def get_pypi_stats(package_name):
    url = f"https://pypistats.org/api/packages/{package_name}/recent"
    response = requests.get(url)
    data = response.json()

    print(f"Recent downloads for {package_name}:")
    print(f"Last day: {data['data']['last_day']}")
    print(f"Last week: {data['data']['last_week']}")
    print(f"Last month: {data['data']['last_month']}")

if __name__ == "__main__":
    get_pypi_stats("neo4j-mcp")
```

#### GitHub Analytics Integration
```yaml
# .github/workflows/analytics.yml
name: Analytics

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  collect-stats:
    runs-on: ubuntu-latest
    steps:
    - name: Collect download stats
      run: |
        curl -s https://api.github.com/repos/${{ github.repository }}/releases | \
        jq -r '.[] | "\(.tag_name): \(.assets[].download_count)"'
```

### User Feedback Collection

#### Telemetry (Optional, with user consent)
```python
# src/neo4j_mcp/telemetry.py
import json
import hashlib
from typing import Optional

class TelemetryCollector:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    def collect_usage_stats(self, event_type: str, metadata: dict):
        if not self.enabled:
            return

        # Anonymize sensitive data
        anonymous_data = {
            "event": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": self._anonymize(metadata)
        }

        # Send to telemetry endpoint
        self._send_telemetry(anonymous_data)

    def _anonymize(self, data: dict) -> dict:
        # Remove or hash sensitive information
        return {k: hashlib.md5(str(v).encode()).hexdigest()[:8]
                if k in ['uri', 'user'] else v
                for k, v in data.items()}
```

---

## 🔒 Security Considerations

### Package Signing

#### GPG Signing
```bash
# Generate GPG key
gpg --gen-key

# Sign package
gpg --detach-sign --armor dist/neo4j_mcp-1.0.0.tar.gz
gpg --detach-sign --armor dist/neo4j_mcp-1.0.0-py3-none-any.whl

# Verify signatures
gpg --verify dist/neo4j_mcp-1.0.0.tar.gz.asc dist/neo4j_mcp-1.0.0.tar.gz
```

#### Supply Chain Security
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Run Bandit security scan
      run: |
        pip install bandit
        bandit -r src/

    - name: Run Safety check
      run: |
        pip install safety
        safety check -r requirements.txt

    - name: SAST with CodeQL
      uses: github/codeql-action/init@v2
      with:
        languages: python
```

### Dependency Management

#### Vulnerability Scanning
```bash
# Check for known vulnerabilities
pip install pip-audit
pip-audit

# Generate software bill of materials (SBOM)
pip install pip-licenses
pip-licenses --format json --output-file sbom.json
```

#### Lock File Management
```bash
# Generate lock file
pip freeze > requirements.lock

# Or use pip-tools
pip install pip-tools
pip-compile requirements.in
```

---

## 🚀 Version Management

### Semantic Versioning Strategy

```
Major.Minor.Patch-PreRelease+BuildMetadata
1.2.3-alpha.1+20240115
```

**Version Bumping Rules:**
- **Major**: Breaking changes to MCP protocol or API
- **Minor**: New features, new tools, backward compatible
- **Patch**: Bug fixes, security patches, documentation
- **Pre-release**: Alpha, beta, rc versions

#### Automated Version Bumping
```bash
# Using bump2version
pip install bump2version

# Configuration in .bumpversion.cfg
[bumpversion]
current_version = 1.0.0
commit = True
tag = True

[bumpversion:file:src/neo4j_mcp/__init__.py]
[bumpversion:file:setup.py]
[bumpversion:file:pyproject.toml]

# Bump version
bump2version patch  # 1.0.0 -> 1.0.1
bump2version minor  # 1.0.1 -> 1.1.0
bump2version major  # 1.1.0 -> 2.0.0
```

### Release Notes Generation

#### Automated Changelog
```bash
# Using git-changelog
pip install git-changelog

# Generate changelog
git-changelog -o CHANGELOG.md

# Or using GitHub CLI
gh api repos/:owner/:repo/releases/generate-notes \
  -f tag_name=v1.0.0 \
  -f target_commitish=main
```

---

## 📈 Success Metrics

### Distribution KPIs

1. **Adoption Metrics:**
   - PyPI downloads per month
   - GitHub stars and forks
   - Docker Hub pulls
   - Active installations (via telemetry)

2. **Quality Metrics:**
   - Test coverage percentage
   - Bug report resolution time
   - Documentation completeness
   - User satisfaction surveys

3. **Community Metrics:**
   - GitHub issues and PRs
   - Discussion participation
   - Community contributions
   - Integration examples shared

### Monitoring and Alerting

```python
# scripts/health_check.py
import requests
import sys

def check_package_health():
    # Check PyPI availability
    response = requests.get("https://pypi.org/project/neo4j-mcp/")
    if response.status_code != 200:
        print("❌ PyPI package not accessible")
        return False

    # Check documentation
    docs_response = requests.get("https://your-username.github.io/neo4j_mcp/")
    if docs_response.status_code != 200:
        print("❌ Documentation site down")
        return False

    print("✅ All distribution channels healthy")
    return True

if __name__ == "__main__":
    if not check_package_health():
        sys.exit(1)
```

---

This comprehensive distribution guide covers all aspects of packaging, building, and distributing the Neo4j MCP server across multiple platforms and channels. Follow the sections relevant to your distribution strategy to ensure users can easily install and use your package in their preferred environment.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Create comprehensive README.md with installation and usage instructions", "activeForm": "Creating comprehensive README.md", "status": "completed"}, {"content": "Write platform-specific installation guides (Windows, Mac, Linux, WSL)", "activeForm": "Writing platform-specific installation guides", "status": "completed"}, {"content": "Document Claude Code integration steps with examples", "activeForm": "Documenting Claude Code integration", "status": "completed"}, {"content": "Create troubleshooting guide for common issues", "activeForm": "Creating troubleshooting guide", "status": "completed"}, {"content": "Add examples and usage scenarios documentation", "activeForm": "Adding examples and usage scenarios", "status": "completed"}, {"content": "Create distribution package documentation", "activeForm": "Creating distribution package documentation", "status": "completed"}]