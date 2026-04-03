import requests
import time
import json

# Убедись, что URL Ngrok актуален!
URL = "https://joinable-capacious-wanita.ngrok-free.dev/api/chat"
HEADERS = {
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true"
}

# Набор тестовых сценариев
TEST_CASES = [
    {"name": "1. Идеальный город", "traffic": 2, "aqi": 30},
    {"name": "2. Час пик", "traffic": 9, "aqi": 80},
    {"name": "3. Экологическая катастрофа", "traffic": 4, "aqi": 250},
    {"name": "4. Полный коллапс", "traffic": 10, "aqi": 350},
    {"name": "5. Проверка на ошибки (Аномалия)", "traffic": -5, "aqi": 9999}
]

def send_request(test_case):
    print(f"🚀 Запуск теста: {test_case['name']} (Трафик: {test_case['traffic']}, AQI: {test_case['aqi']})")
    
    # Слово "Пробки" нейросеть никогда не спутает с английским
    user_prompt = F"Уровень пробок = {test_case['traffic']} баллов, AQI = {test_case['aqi']}."
    
    # === ГЛАВНЫЕ ИЗМЕНЕНИЯ ЗДЕСЬ ===
    payload = {
        "model": "mayor-ai",  # Вызываем твою личную сборку!
        "format": "json",     # Требуем формат JSON через API
        "messages": [
            {"role": "user", "content": user_prompt} # Системного промпта больше нет
        ],
        "stream": False
    }

    start_time = time.time()
    try:
        response = requests.post(URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        end_time = time.time()
        
        raw_reply = response.json().get("message", {}).get("content", "{}")
        
        # Пытаемся распарсить JSON
        try:
            parsed_json = json.loads(raw_reply.strip().strip('```json').strip('```'))
            is_valid_json = True
        except json.JSONDecodeError:
            parsed_json = raw_reply
            is_valid_json = False

        duration = round(end_time - start_time, 2)
        return {
            "name": test_case["name"],
            "duration": duration,
            "success": True,
            "valid_json": is_valid_json,
            "reply": parsed_json
        }
    except Exception as e:
        end_time = time.time()
        return {
            "name": test_case["name"],
            "duration": round(end_time - start_time, 2),
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    print("=== СТАРТ СТРЕСС-ТЕСТА ДЛЯ МОДЕЛИ 'mayor-ai' ===\n")
    
    # Запускаем запросы последовательно
    for case in TEST_CASES:
        result = send_request(case)
        if result["success"]:
            print(f"✅ Успех ({result['duration']} сек)")
            print(f"JSON валиден: {'Да' if result['valid_json'] else 'НЕТ'}")
            print(f"Ответ ИИ: {json.dumps(result['reply'], ensure_ascii=False, indent=2)}\n")
        else:
            print(f"❌ ОШИБКА ({result['duration']} сек): {result['error']}\n")
            
    print("=== ТЕСТ ЗАВЕРШЕН ===")