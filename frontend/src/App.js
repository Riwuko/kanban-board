import React from "react";
import Registration from "./components/Registration";
import { BrowserRouter, Route } from "react-router-dom";
import "./styles/styles.css";
import { ThemeProvider } from "@chakra-ui/core";

const App = () => {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Route path="/register" component={Registration} />
      </BrowserRouter>
    </ThemeProvider>
  );
};

export default App;
