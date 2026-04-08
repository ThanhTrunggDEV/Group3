# Gold Price Forecaster API 📈

An advanced Machine Learning project developed by **Group 3** to predict gold prices (`Close` price) based on financial metrics. Built with ML.NET (LightGBM) and deployed as a lightning-fast ASP.NET Core Web API with a premium web interface.

## 👥 Team Members
- Nguyen Thanh Trung
- Do Van Nguyen
- Nguyen Xuan Huong
- Nguyen Quoc Dat

## 🚀 Fast Deployment (Docker)

To deploy the fully containerized application on a Linux Server (VPS), simply run the following command. It will automatically pull the newest Git snapshot from the GitHub Container Registry and run it on port `5235`.

```bash
sudo docker rm -f goldprice_api || true && sudo docker run -d --name goldprice_api --restart unless-stopped --pull always -p 5235:8080 -e ASPNETCORE_ENVIRONMENT=Production -e ASPNETCORE_URLS="http://+:8080" ghcr.io/thanhtrunggdev/group3:latest
```

Once running, access the user interface at: 
👉 `http://<your-server-ip>:5235/index.html`

*(Swagger Developer API is available at `/swagger`)*

## 🛠 Technical Features
- **Machine Learning**: Custom-trained LightGBM Regressor using `Microsoft.ML`.
- **Backend API**: Minimal API built with .NET 10 featuring built-in Rate Limiting.
- **Frontend UI**: Integrated modern Glassmorphism dark-mode HTML/CSS/JS interface.
- **DevOps**: Fully automated CI/CD pipeline building to GHCR via GitHub Actions.

## 📊 References & Dataset
Repository used to compare the results and references (includes dataset):
[https://github.com/mahu21/GoldPrice](https://github.com/mahu21/GoldPrice)
