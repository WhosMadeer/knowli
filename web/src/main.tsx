import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import { Upload } from "./app/file-upload/upload";
import App from "./App";
import Calendar from "./app/calendar";
import "./index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route index element={<Upload />} />
        <Route path="/app" element={<App />} />
        <Route path="/cal" element={<Calendar />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
