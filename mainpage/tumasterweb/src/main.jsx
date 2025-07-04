import { createBrowserRouter, RouterProvider } from "react-router";
import { createRoot } from "react-dom/client";
import IndexPage from "./IndexPage.jsx";
import CoursePage from "./CoursePage.jsx";
import LearningPaths from "./LearningPaths.jsx";
import AboutPage from "./AboutPage.jsx";
import LoginPage from "./LoginPage.jsx";
import ForgotPasswordPage from "./ForgotPasswordPage.jsx";
import RegisterPage from "./RegisterPage.jsx";
import "./main.css";

const router = createBrowserRouter([
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
]);

createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />
);
