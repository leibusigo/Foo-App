import Login from '../pages/Login'
import Main from '../pages/Main'
import AI from '../pages/Main/AI'
import Home from '../pages/Main/Home'

const routerConfig = [
  {
    path: '',
    element: <Main />,
    children: [
      {
        path: '',
        element: <Home />,
      },
      {
        path: 'algorithm',
        element: <AI />,
      },
    ],
  },
  {
    path: '/login',
    element: <Login />,
  },
]

export default routerConfig
