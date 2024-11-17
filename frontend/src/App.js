import React, { useState } from "react";
import { Box, CssBaseline, Container, Typography } from "@mui/material";
import Login from "./components/login";
import Home from "./components/home";
import { ThemeProvider, createTheme } from "@mui/material/styles";



const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userInfo, setUserInfo] = useState(null);
  const [refreshToken, setRefreshToken] = useState(null);

  const handleLogin = (result) => {
    
    setUserInfo({...result,isAdmin:result?.employee?.id === 1})
    console.log({...result,isAdmin:result?.employee?.id === 1})
    setIsAuthenticated(true); // Giriş yapıldığında ana sayfaya geçiş
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main">
        <CssBaseline />

        {!isAuthenticated ? (
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              marginTop: "15%",
            }}
          >
            <Typography variant="h1" color="secondary" gutterBottom >İHA ÜRETİM UYGULAMASI</Typography>
            <Login onLogin={handleLogin} />
          </Box>
        ) : (
          <Home userInfo={userInfo}/>
        )}
      </Container>
    </ThemeProvider>
  );
};

export default App;

const theme = createTheme({
  palette: {
    primary: {
      main: "#021d62", 
      light: "#25478a",
      dark: "#000940", 
      contrastText: "#ffffff", 
    },
    secondary: {
      main: "#6c757d", 
      light: "#a0a4a8",
      dark: "#494e52", 
      contrastText: "#ffffff",
    },
    background: {
      default: "#f4f6f8", 
      paper: "#ffffff",   
    },
    text: {
      primary: "#021d62", 
      secondary: "#6c757d",
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Arial', sans-serif",
    h1: { fontSize: "2rem", fontWeight: 700 },
    h2: { fontSize: "1.5rem", fontWeight: 600 },
    body1: { fontSize: "1rem", fontWeight: 400 },
  },
});

// const fetchData = async () => {
//   try {
//     const response = await fetch("http://localhost:8000/api/protected/", {
//       method: "GET",
//       headers: {
//         Authorization: `Bearer ${accessToken}`,
//       },
//     });

//     const data = await response.json();
//     if (response.ok) {
//       console.log("Veri:", data);
//     } else {
//       console.error("API hatası:", data);
//     }
//   } catch (error) {
//     console.error("Veri çekme hatası:", error);
//   }
// };
