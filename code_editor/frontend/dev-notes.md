## Node version

This frontend package compiles with warnings using node version `v16.17.0`.
You can list installed node versions using `nvm ls`. To use a specific version that is installed, you can use `nvm use <version>`. For example, `nvm use 16.17.0`.

---

## Vulnerabilities 

If you run any npm command like `npm install`, you will see a list of vulnerabilities. There is no point in fixing these vulnerabilities as most of them stem from `react-scripts` and are known to not have any relevancy to this type of project. To skip these vulnerabilities, make sure `react-scripts` is in the devDependencies and then run `npm audit --production`.