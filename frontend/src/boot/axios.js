import { boot } from 'quasar/wrappers'
import axios from 'axios' 

const api = axios.create({ baseURL: 'http://192.168.0.110:8000' })

export default boot(({ app }) => {
  app.config.globalProperties.$api = api
  app.config.globalProperties.$axios = axios
})

export { api }

