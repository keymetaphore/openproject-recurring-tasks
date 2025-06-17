# An extremely simple and rudimentary task scheduler for Openproject.
OpenProject, for a reason unbeknownst to man, does not support recurring tasks (work packages) since it was suggested and added to backlog in 2020. Through an anger fueled evening, this quick project was made to run as an external Docker service, call the OpenProject API and create predefined tasks in a cron format.

The project does support OIDC and in fact, that is the only authentication method (besides there being no authentication at all). It simply is what I use (with Keycloak, though you may use any OpenID provider as it will fetch the .well_known/openid_configuration file). You may run the software without OIDC, but take note that anyone with access to the panel will be able to use it with your API key. Or, you may of course implement another authentication method. The code is extremely simple, so if you do, please make a PR.

# Installation
1. Clone the Github repository
```bash
git clone https://github.com/keymetaphore/openproject-recurring-tasks.git
cd openproject-recurring-tasks
```
2. Create the .env file and populate. If you wish to use OIDC, enable it, otherwise, leave it on false. Caution! If it is set to false and you do not set up your own authentication on a reverse proxy, *anyone* that can reach this panel will be able to use it. There is no other access control implemented.
```bash
cp env.example .env
nano .env
```
3. If using SElinux, grant svirt_sandbox_file_t access.
```bash
sudo chcon -Rt svirt_sandbox_file_t .
```
4. Start the server.
```bash
docker compose up -d
```

# Usage

The panel is dead simple. It uses cron style strings to schedule tasks. You may specify the title, description, and assigned person. Description supports markdown. That is it. It is trivial to expand if you need more features, and if you do, of course, you are welcome to submit a PR.