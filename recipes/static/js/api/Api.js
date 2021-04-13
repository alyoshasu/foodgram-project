class Api {
  constructor() {
    this.apiUrl = '/api/v1';
    this.headers = {
      'Content-Type': 'application/json'
    };
  }

  fetch(url, method, body) {
    console.time(`Request ${method || 'GET'} => ${url}`)
    return fetch(`${this.apiUrl}${url}`, {
      headers: this.headers,
      method: method || 'GET',
      body: body || undefined
    }).then(e => {
      if (e.ok) {
        return e.json()
      }
      return Promise.reject(e.statusText)
    }).finally(() => console.timeEnd(`Request ${method || 'GET'} => ${url}`))
  }

  getPurchases() {
    return this.fetch('/purchases')
  }

  addPurchases(id) {
    return this.fetch(`${this.apiUrl}/purchases`, 'POST', JSON.stringify({
      id: id
    }))
  }

  removePurchases(id) {
    return this.fetch(`${this.apiUrl}/purchases/${id}`, 'DELETE')
  }

  addSubscriptions(id) {
    return this.fetch(`${this.apiUrl}/subscriptions`, 'POST', JSON.stringify({
      id: id
    }))
  }

  removeSubscriptions(id) {
    return this.fetch(`${this.apiUrl}/subscriptions/${id}`, 'DELETE')
  }

  addFavorites(id) {
    return this.fetch(`${this.apiUrl}/favorites`, 'POST', JSON.stringify({
      id: id
    }))

  }

  removeFavorites(id) {
    return this.fetch(`${this.apiUrl}/favorites/${id}`, 'DELETE')
  }

  getIngredients(text) {
    return this.fetch(`/ingredients?search=${text}`)
  }
}
