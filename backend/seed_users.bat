@echo off
echo 🌱 Running CoinCraft User Seeding Script...
echo.

cd /d "%~dp0"
uv run seed_users.py

echo.
echo ✅ Seeding complete! Press any key to exit...
pause >nul
