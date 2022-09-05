import Login from '../pages/Login'
import Main from '../pages/Main'

const routerConfig = [
  {
    path: '',
    element: <Main />,
  },
  {
    path: '/login',
    element: <Login />,
  },
]

export default routerConfig
