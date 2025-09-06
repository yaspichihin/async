.PHONY: help lint format check fix clean

help:
	@echo "Доступные команды:"
	@echo "  format    - Исправить все возможные проблемы"
	@echo "  clean     - Очистить кэш и временные файлы"

fix:
	@echo "🔧 Сортируем импорты..."
	isort .
	@echo "🔧 Исправляем проблемы с помощью ruff..."
	ruff check --fix .
	@echo "🔧 Форматируем код..."
	ruff format .

clean:
	@echo "🧹 Очищаем кэш..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✨ Кэш очищен!"
