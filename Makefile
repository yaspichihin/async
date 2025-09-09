fix:
	@echo "🔧 Сортируем импорты..."
	isort src/
	@echo "🔧 Исправляем проблемы с помощью ruff..."
	ruff check --fix src/
	@echo "🔧 Форматируем код..."
	ruff format src/
	@echo "🔧 Выполняем dos2unix"
	find src/ -type f -name "*.py" | xargs dos2unix
	@echo "🧹 Очищаем кэш..."
	find src/ -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find src/ -type f -name "*.pyc" -delete 2>/dev/null || true
	find src/ -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✨ Кэш очищен!"
