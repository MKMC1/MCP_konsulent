# MCP Konsulent Staffing

Dette prosjektet er en enkel MCP-løsning med to mikrotjenester:
- **konsulent-api**: Tilbyr en liste over konsulenter.
- **llm-verktøy-api**: Filtrerer konsulenter og returnerer et sammendrag basert på tilgjengelighet og ferdigheter.

## 🚀 Kom i gang

### Windows
1. Installer og start Docker Desktop.
2. Åpne terminal (PowerShell, CMD eller VS Code).
3. Kjør:
   ```sh
   docker compose up --build
   ```

### Linux/Mac
1. Installer Docker.
2. Sørg for at Docker daemon kjører (`sudo systemctl start docker` hvis nødvendig).
3. Kjør:
   ```sh
   docker compose up --build
   ```

4. Gå til localhost:8002/docs i en nettleser.
5. Trykk på GET fanen for å frem UI og trykk på Try it out knappen.
6. Fyll ut minimum tilgjengelig prosent og påkrevd ferdighet (eventuelt velg modell) og trykk execute.
7. Gå ned til responses og response body for å se sammendraget i JSON-format.
8. Kjør docker compose down for å fjerne konteinere.

Testkjøring:
   ```bash```
   docker compose run konsulent-api pytest
   docker compose run llm-verktoy-api pytest