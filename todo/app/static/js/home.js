//axios.defaults.xsrfHeaderName = "X-CSRFToken"
//axios.defaults.xsrfCookieName = "csrftoken"

//console.log('HomeItems')

//let HomeItems = JSON.parse(document.getElementById('items_vue').textContent)
//let HomeItems = JSON.parse(document.getElementById('items_vue'));
//console.log(storage)
//console.log(HomeItems)



const appVue = Vue.createApp({
    
    data() {
        return {
            csrf: null,
            task: {title: ''},
            tasks: [],
            
        }
    },

    methods: {
        async sendRequest(url, method, data) {
            let myHeaders = new Headers({
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            })

            if(method !== 'get') {
                myHeaders.set('X-CSRFToken', await this.getCsrfToken())
            }

            let response = await fetch(url, {
                method: method,
                headers: myHeaders,
                body: data
            })

            return response
            
        },

        async getCsrfToken () {
            if(this.csrf === null) {
                let response = await this.sendRequest('http://127.0.0.1:8000/csrf/', 'get')
                let data = await response.json()
                this.csrf = data.csrf_token
            }
            return this.csrf
        },
        
        async getTasks() {
            let response = await this.sendRequest('http://127.0.0.1:8000/task/', 'get')
            this.tasks = await response.json()
        },

        async createTask() {
            await this.getTasks()

            await this.sendRequest('http://127.0.0.1:8000/task/', 'post', JSON.stringify(this.task))

            this.task.title = ''
            await this.getTasks()
        },

        async deleteTask(task) {
            await this.sendRequest('http://127.0.0.1:8000/task/', 'delete', JSON.stringify(task))

            await this.getTasks()
        },

        async completedTask(task) {
            console.log(111)
            await this.sendRequest('http://127.0.0.1:8000/task/', 'put', JSON.stringify(task))

            await this.getTasks()
        }
        
    },

    filters: {
        time: function (value) {
            return value.toLocaleString()
        }
    },

    async created(){
        await this.getTasks()
    }
    

})

appVue.config.compilerOptions.delimiters = [ '[[', ']]' ]
const mountedApp = appVue.mount('#app')