import * as React from 'react';
import Box from '@mui/material/Box';
import AppBarComponent from './appBarComponent';
import UawPage from './homePages/uawPage';
import TeamsPage from './homePages/teamsPage';
import PartsPage from './homePages/partsPage';
import MontagePage from './homePages/montagePage';


import { useState } from 'react';
import { Paper } from '@mui/material';

const Home = () => {

  const [currentPage, setCurrentPage] = useState("uaw")

  const pages = [
    { id: "uaw", name: "İHA Envanteri", desc: "İnsansız Hava Araçlarının listesi ve bilgileri" },
    { id: "teams", name: "Takımlar", desc: "Farklı takımlar ve görev dağılımlarının detayları" },
    { id: "parts", name: "Parçalar", desc: "Montajda kullanılan bileşenler ve ekipmanlar" },
    { id: "montage", name: "Montaj", desc: "Montaj işlemleri" }
  ];

  return (
    <Box>
      <AppBarComponent pages={pages} currentPage={currentPage} setCurrentPage={setCurrentPage} />

      <Box sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginTop: "15%",
      }}>
        <Paper elevation={3} sx={{width:"100%"}}>
          {currentPage === "uaw" && <UawPage />}
          {currentPage === "teams" && <TeamsPage />}
          {currentPage === "parts" && <PartsPage />}
          {currentPage === "montage" && <MontagePage />}
        </Paper>
      </Box>
    </Box>
  );
}
export default Home;