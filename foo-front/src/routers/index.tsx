import Login from '../pages/Login'
import Main from '../pages/Main'
import AI from '../pages/Main/AI'
import Home from '../pages/Main/Home'
import NotFound from '../pages/NotFound'

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
  {
    path: '/notFound',
    element: <NotFound />,
  },
]

export default routerConfig
