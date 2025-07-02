import "./main.css";
import { createRoot } from "react-dom/client";
import IndexPage from "./IndexPage.jsx";
import CoursePage from "./CoursePage.jsx";
import LearningPaths from "./LearningPaths.jsx";
import AboutPage from "./AboutPage.jsx";
import { createBrowserRouter, RouterProvider } from "react-router";

const router = createBrowserRouter([
  {
    path: "/",
    element: <IndexPage />,
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
