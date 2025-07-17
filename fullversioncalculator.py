<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Calculator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            padding: 20px;
        }
        
        .calculator-container {
            width: 100%;
            max-width: 400px;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            overflow: hidden;
            border: 1px solid #444;
        }
        
        .display {
            background: #111;
            padding: 30px 20px;
            text-align: right;
            position: relative;
            border-bottom: 1px solid #333;
        }
        
        .operation-display {
            color: #aaa;
            font-size: 1.2rem;
            min-height: 25px;
            overflow-x: auto;
            white-space: nowrap;
        }
        
        .result-display {
            color: #fff;
            font-size: 3rem;
            font-weight: 300;
            margin-top: 10px;
            min-height: 60px;
            overflow-x: auto;
            white-space: nowrap;
        }
        
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1px;
            background: #333;
        }
        
        .btn {
            border: none;
            outline: none;
            padding: 20px 10px;
            font-size: 1.5rem;
            background: #222;
            color: #fff;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .btn:hover {
            background: #333;
        }
        
        .btn:active {
            background: #444;
            transform: scale(0.95);
        }
        
        .operator {
            background: #333;
            color: #ff9500;
            font-weight: 500;
        }
        
        .operator:hover {
            background: #444;
        }
        
        .equals {
            background: #ff9500;
            color: #fff;
            grid-column: span 2;
        }
        
        .equals:hover {
            background: #ffaa33;
        }
        
        .special {
            background: #1a1a1a;
            color: #ff5e5e;
        }
        
        .zero {
            grid-column: span 2;
        }
        
        .history-btn {
            position: absolute;
            top: 15px;
            left: 20px;
            background: #333;
            color: #aaa;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .history-btn:hover {
            background: #444;
            color: #fff;
        }
        
        .history-panel {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            padding: 20px;
            overflow-y: auto;
            transform: translateX(-100%);
            transition: transform 0.4s ease;
        }
        
        .history-panel.active {
            transform: translateX(0);
        }
        
        .history-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            color: #fff;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
        }
        
        .close-history {
            background: none;
            border: none;
            color: #aaa;
            font-size: 1.5rem;
            cursor: pointer;
        }
        
        .history-item {
            padding: 10px 0;
            border-bottom: 1px solid #222;
            color: #ddd;
        }
        
        .history-calculation {
            color: #aaa;
            font-size: 0.9rem;
        }
        
        .history-result {
            font-size: 1.2rem;
            color: #ff9500;
            text-align: right;
        }
        
        @media (max-width: 480px) {
            .calculator-container {
                max-width: 100%;
            }
            
            .btn {
                padding: 15px 5px;
                font-size: 1.3rem;
            }
            
            .result-display {
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="calculator-container">
        <div class="display">
            <button class="history-btn">📜</button>
            <div class="operation-display"></div>
            <div class="result-display">0</div>
            
            <div class="history-panel">
                <div class="history-header">
                    <h3>Calculation History</h3>
                    <button class="close-history">✕</button>
                </div>
                <div class="history-list">
                    <!-- History items will be added here -->
                </div>
            </div>
        </div>
        
        <div class="buttons">
            <button class="btn special" data-action="clear">C</button>
            <button class="btn special" data-action="backspace">⌫</button>
            <button class="btn special" data-action="percent">%</button>
            <button class="btn operator" data-operator="÷">÷</button>
            
            <button class="btn" data-number="7">7</button>
            <button class="btn" data-number="8">8</button>
            <button class="btn" data-number="9">9</button>
            <button class="btn operator" data-operator="×">×</button>
            
            <button class="btn" data-number="4">4</button>
            <button class="btn" data-number="5">5</button>
            <button class="btn" data-number="6">6</button>
            <button class="btn operator" data-operator="-">−</button>
            
            <button class="btn" data-number="1">1</button>
            <button class="btn" data-number="2">2</button>
            <button class="btn" data-number="3">3</button>
            <button class="btn operator" data-operator="+">+</button>
            
            <button class="btn zero" data-number="0">0</button>
            <button class="btn" data-number=".">.</button>
            <button class="btn equals">=</button>
        </div>
    </div>

    <script>
        // Calculator state
        let currentOperand = '';
        let previousOperand = '';
        let operation = null;
        let shouldResetScreen = false;
        let calculationHistory = [];

        // DOM Elements
        const resultDisplay = document.querySelector('.result-display');
        const operationDisplay = document.querySelector('.operation-display');
        const historyList = document.querySelector('.history-list');
        const historyPanel = document.querySelector('.history-panel');
        const historyBtn = document.querySelector('.history-btn');
        const closeHistoryBtn = document.querySelector('.close-history');
        
        // Button elements
        const numberButtons = document.querySelectorAll('[data-number]');
        const operatorButtons = document.querySelectorAll('[data-operator]');
        const equalsButton = document.querySelector('.equals');
        const clearButton = document.querySelector('[data-action="clear"]');
        const backspaceButton = document.querySelector('[data-action="backspace"]');
        const percentButton = document.querySelector('[data-action="percent"]');

        // Event Listeners
        numberButtons.forEach(button => {
            button.addEventListener('click', () => appendNumber(button.textContent));
        });

        operatorButtons.forEach(button => {
            button.addEventListener('click', () => setOperation(button.dataset.operator));
        });

        equalsButton.addEventListener('click', calculate);
        clearButton.addEventListener('click', clear);
        backspaceButton.addEventListener('click', backspace);
        percentButton.addEventListener('click', percent);
        historyBtn.addEventListener('click', () => historyPanel.classList.add('active'));
        closeHistoryBtn.addEventListener('click', () => historyPanel.classList.remove('active'));

        // Keyboard support
        document.addEventListener('keydown', e => {
            if (e.key >= 0 && e.key <= 9) appendNumber(e.key);
            if (e.key === '.') appendNumber(e.key);
            if (e.key === '=' || e.key === 'Enter') calculate();
            if (e.key === 'Backspace') backspace();
            if (e.key === 'Escape') clear();
            if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/') {
                setOperation(
                    e.key === '*' ? '×' : 
                    e.key === '/' ? '÷' : e.key
                );
            }
        });

        // Calculator functions
        function appendNumber(number) {
            if (resultDisplay.textContent === '0' || shouldResetScreen) {
                resetScreen();
            }
            
            // Prevent multiple decimal points
            if (number === '.' && currentOperand.includes('.')) return;
            
            currentOperand += number;
            updateDisplay();
        }

        function resetScreen() {
            currentOperand = '';
            shouldResetScreen = false;
        }

        function updateDisplay() {
            resultDisplay.textContent = currentOperand || '0';
            
            if (operation) {
                operationDisplay.textContent = `${previousOperand} ${operation} ${currentOperand}`;
            } else {
                operationDisplay.textContent = previousOperand;
            }
        }

        function setOperation(op) {
            if (currentOperand === '') return;
            if (previousOperand !== '') {
                calculate();
            }
            
            operation = op;
            previousOperand = currentOperand;
            shouldResetScreen = true;
            updateDisplay();
        }

        function calculate() {
            if (operation === null || shouldResetScreen) return;
            if (currentOperand === '0' && operation === '÷') {
                alert("Division by zero is not allowed!");
                clear();
                return;
            }
            
            let computation;
            const prev = parseFloat(previousOperand);
            const current = parseFloat(currentOperand);
            
            switch (operation) {
                case '+':
                    computation = prev + current;
                    break;
                case '−':
                    computation = prev - current;
                    break;
                case '×':
                    computation = prev * current;
                    break;
                case '÷':
                    computation = prev / current;
                    break;
                default:
                    return;
            }
            
            // Add to history
            addToHistory(`${previousOperand} ${operation} ${currentOperand}`, computation);
            
            currentOperand = computation.toString();
            operation = null;
            previousOperand = '';
            shouldResetScreen = true;
            updateDisplay();
        }

        function addToHistory(calculation, result) {
            calculationHistory.unshift({ calculation, result });
            
            // Update history display
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.innerHTML = `
                <div class="history-calculation">${calculation}</div>
                <div class="history-result">${result}</div>
            `;
            
            historyList.prepend(historyItem);
            
            // Keep only 10 items in history
            if (calculationHistory.length > 10) {
                calculationHistory.pop();
                if (historyList.children.length > 10) {
                    historyList.removeChild(historyList.lastChild);
                }
            }
        }

        function clear() {
            currentOperand = '';
            previousOperand = '';
            operation = null;
            updateDisplay();
        }

        function backspace() {
            currentOperand = currentOperand.slice(0, -1);
            if (currentOperand === '') currentOperand = '0';
            updateDisplay();
        }

        function percent() {
            if (currentOperand === '') return;
            currentOperand = (parseFloat(currentOperand) / 100;
            updateDisplay();
        }

        // Initialize display
        updateDisplay();
    </script>
</body>
</html>
