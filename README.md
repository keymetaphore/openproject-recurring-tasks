# OpenProject Recurring Tasks Scheduler

**A dead-simple external scheduler for OpenProject recurring tasks.**

OpenProject has [no built-in support for recurring work packages](https://community.openproject.org/work_packages/36463) for 5 years since suggested. This lightweight and dockerized tool bridges that gap by running externally and triggering OpenProject API calls using cron expressions you define.

Supports optional OpenID Connect (OIDC) authentication (e.g. Keycloak). Use at your own risk if exposing the panel without proper access control.

Please take into account that the development of this tool was fueled by anger by not having such a basic feature as recurring work packages available.

---

## Features

- Define recurring tasks using cron syntax (e.g. `0 15 * * *`)
- OIDC login support (e.g. Keycloak, Auth0, ADFS)
- Rich markdown support for task descriptions
- Assign tasks to users

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/keymetaphore/openproject-recurring-tasks.git
cd openproject-recurring-tasks
```

### 2. Create and configure the environment

```bash
cp env.example .env
nano .env
```

**Required values:**

| Variable               | Description                                                   |
|------------------------|---------------------------------------------------------------|
| `OPENPROJECT_API_TOKEN`| Your OpenProject API key from /my/access_token                |
| `OPENPROJECT_BASE_URL` | Base URL to your OpenProject instance                         |
| `OIDC_ENABLED`         | `true` or `false`. Next 4 values not mandatory if false.      |
| `OIDC_CLIENT_ID`       | Client ID from your OIDC provider                             |
| `OIDC_CLIENT_SECRET`   | Client secret from your OIDC provider                         |
| `OIDC_ISSUER_URL`      | Issuer URL (ends in `/realms/...`)                            |
| `OIDC_REDIRECT_URI`    | Full redirect URI (e.g. `https://example.com/auth/callback`)  |
| `APP_NAME`             | Name displayed in UI header                                   |
| `APP_LOGO_URL`         | Logo URL shown in header bar                                  |
| `SECRET_KEY`           | Random string for session security                            |

### 3. (Optional) Adjust SELinux file context, if you use SELinux.

```bash
sudo chcon -Rt svirt_sandbox_file_t .
```

### 4. Launch with Docker Compose

```bash
docker compose up -d
```


## 🛠 Usage

1. Visit the dashboard.
2. Create a new task:
   - Provide a **title**, **cron expression**, **project**, **user**, and **optional description**.
   - Cron format is standard 5-part: `minute hour day month day-of-week`
3. The task will auto-schedule and create OpenProject work packages at the specified intervals.

> You can edit, suspend, resume, or delete existing scheduled tasks directly from the dashboard.

If you use it and care enough, please make a screenshot of the interface and PR it. 

---

## Authentication Notes

- If `OIDC_ENABLED=true`, the app enforces OpenID Connect login.
- If `OIDC_ENABLED=false`, **no authentication is applied**. Anyone with access to the web UI can use your API key.
  - Protect the interface using a reverse proxy with access controls. 


---

## Contributing

Pull requests are welcome and encouraged. I /know/ I am not the only one who had this issue, so if this project was useful and you did something to improve it, please, make a PR.

- Supporting additional OpenProject fields
- UI/UX improvements
- Improved authentication strategies
- Tests and documentation (please)

---

## Disclaimer

This is a community tool built to fill a gap in OpenProject. It is not affiliated with OpenProject. Use at your own risk, especially if you do not implement authentication.
AI disclaimer: Part of this README and the user interface was generated using AI. All backend code and infrastructure was written by hand.

---

## License

BSD-3 License. See [`LICENSE`](LICENSE.md) for details.

Contact: Kevins17 <kevins17@lidmasina.lv>