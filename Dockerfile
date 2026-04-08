# 1. Buid Stage: Use the official .NET SDK image
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Copy project file and restore dependencies
COPY ["GoldPrice_API/GoldPrice_API.csproj", "GoldPrice_API/"]
RUN dotnet restore "GoldPrice_API/GoldPrice_API.csproj"

# Copy the entire solution to build it
COPY . .

# Build and publish the API project
WORKDIR "/src/GoldPrice_API"
RUN dotnet publish "GoldPrice_API.csproj" -c Release -o /app/publish /p:UseAppHost=false

# 2. Runtime Stage: Use the official ASP.NET Core runtime image
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final

# We need the relative path logic to work:
# API runs from /app/GoldPrice_API
# Model is expected at /app/GoldPrice_CLI/GoldModel.zip

# Create and copy the model
WORKDIR /app/GoldPrice_CLI
COPY --from=build /src/GoldPrice_CLI/GoldModel.zip .

# Copy the published API
WORKDIR /app/GoldPrice_API
COPY --from=build /app/publish .

# Expose standard HTTP port
EXPOSE 8080

# Run the API
ENTRYPOINT ["dotnet", "GoldPrice_API.dll"]
