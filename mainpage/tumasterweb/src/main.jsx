import { createBrowserRouter, RouterProvider } from "react-router";
import { createRoot } from "react-dom/client";
import "./main.css";
import App from "./App.jsx";
import IndexPage from "./IndexPage.jsx";
import CoursePage from "./CoursePage.jsx";
import LearningPaths from "./LearningPaths.jsx";
import AboutPage from "./AboutPage.jsx";
import LoginPage from "./LoginPage.jsx";
import ForgotPasswordPage from "./ForgotPasswordPage.jsx";
import RegisterPage from "./RegisterPage.jsx";
import { store } from "./store/index.js";
import { Provider } from "react-redux";

const router = createBrowserRouter([
  {
    element: <App />,
    children: [
      {
        path: "/",
        element: <IndexPage />,
      },
      {
        path: "/login",
        element: <LoginPage />,
      },
      {
        path: "/forgot_password",
        element: <ForgotPasswordPage />,
      },
      {
        path: "/register",
        element: <RegisterPage />,
      },
      {
        path: "/course",
        element: <CoursePage />,
      },
      {
        path: "/learning_paths",
        element: <LearningPaths />,
      },
      {
        path: "/about",
        element: <AboutPage />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  <Provider store={store}>
    <RouterProvider router={router} />
  </Provider>
);
