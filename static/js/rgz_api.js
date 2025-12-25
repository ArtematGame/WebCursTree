// static/js/rgz_api.js

// Базовые функции для работы с JSON-RPC API
function callRpcMethod(method, params = {}) {
    const url = '/rgz/json-rpc-api/';
    const json = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': Math.round(Math.random()*1000)
    };
    
    return fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(json)
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.error) {
            console.error('RPC Error:', data.error);
            throw new Error(data.error.message || 'Unknown error');
        }
        return data.result;
    });
}

// Функция для загрузки информации о пользователе
function loadUserInfo() {
    return callRpcMethod('get_user_info')
        .then(function(user) {
            return user;
        })
        .catch(function(error) {
            if (error.message === 'Unauthorized') {
                return null; // Пользователь не авторизован
            }
            console.error('Failed to load user info:', error);
            throw error;
        });
}

// Функция для выполнения входа
function performLogin(login, password) {
    return callRpcMethod('login', {login: login, password: password});
}

// Функция для выполнения перевода
function performTransfer(toAccount, amount, description) {
    return callRpcMethod('transfer', {
        to_account: toAccount,
        amount: amount,
        description: description
    });
}

// Функция для загрузки транзакций
function loadTransactions() {
    return callRpcMethod('get_transactions');
}

// Функция для загрузки всех пользователей (для менеджеров)
function loadAllUsers() {
    return callRpcMethod('get_all_users');
}

// Функция для создания пользователя (для менеджеров)
function createUser(userData) {
    return callRpcMethod('create_user', userData);
}

// Функция для выхода
function performLogout() {
    return callRpcMethod('logout')
        .then(function(result) {
            window.location.href = '/rgz';
        });
}