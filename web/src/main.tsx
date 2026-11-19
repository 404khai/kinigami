import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "allo-font/allo.css";
import "@fontsource-variable/jetbrains-mono";
import "./styles.css";
import { Blog } from "./blog/BlogPage";
import { Blueprint } from "./components/Blueprint";
import { Home } from "./home/Home";
import { useLinkInterception, usePath } from "./lib/router";

// Routes: / (overview), /blog, /blog/:slug.
function Root() {
  useLinkInterception();
  const path = usePath().replace(/\/+$/, "") || "/";
  const blog = path.match(/^\/blog(?:\/([^/]+))?$/);
  return (
    <>
      <Blueprint />
      {blog ? <Blog slug={blog[1] && decodeURIComponent(blog[1])} /> : <Home />}
    </>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Root />
  </StrictMode>,
);
