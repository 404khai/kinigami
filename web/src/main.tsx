import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@fontsource-variable/bricolage-grotesque";
import "@fontsource-variable/jetbrains-mono";
import "./styles.css";
import { Blog } from "./blog/BlogPage";
import { Docs } from "./docs/DocsPage";
import { Home } from "./home/Home";
import { useLinkInterception, usePath } from "./lib/router";

// Routes: / (overview), /docs (#page), /blog, /blog/:slug.
function Root() {
  useLinkInterception();
  const path = usePath().replace(/\/+$/, "") || "/";
  const blog = path.match(/^\/blog(?:\/([^/]+))?$/);
  return (
    <>{blog ? <Blog slug={blog[1] && decodeURIComponent(blog[1])} /> : path === "/docs" ? <Docs /> : <Home />}</>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Root />
  </StrictMode>,
);
