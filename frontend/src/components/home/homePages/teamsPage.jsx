import { Box, Grid2, Tab, Tabs, Typography } from '@mui/material'
import React, { Fragment, useEffect, useState } from 'react'
import MUIDataTable from "mui-datatables";
import { language } from '../../../utils/dataTableOptions';

function TeamPage() {

  // tab
  const [tabValue, setTabValue] = useState(5);
  const [tabs, setTabs] = useState([]);


  const [data, setData] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(false);

  // API'den veri çekmek için fonksiyon
  const fetchData = async (newTabValue = null) => {
    setLoading(true);
    const team = newTabValue ? newTabValue : tabValue;
    fetch(`http://127.0.0.1:8000/api/employees/${team}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setData(data.map((item) => [
          item.name,
          item.team_name.name,
        ]));
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      }).finally(() => setLoading(false));
  };

  const fetchTeamInfo = () => {
    setLoading(true)
    fetch('http://127.0.0.1:8000/api/teams-list/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setTabs(data)
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      }).finally(() => setLoading(false));
  }

  // Tablo ayarları
  const options = {
    count: totalRecords,
    rowsPerPage: 10,
    rowsPerPageOptions: [10, 20, 50],
    selectableRows: "none",
    textLabels: language,
  };


  const handleTabValueChange = (event, newValue) => {
    setTabValue(newValue);
    fetchData(newValue);
  };


  useEffect(() => {
    fetchTeamInfo();
    fetchData();
  }, []);


  return (
    <Box>
      <Box sx={{ width: '100%', borderBottom: 1, borderColor: 'divider', p: 2 }} >
        <Tabs
          variant="fullWidth"
          onChange={handleTabValueChange}
          value={tabValue}
          textColor="secondary"
          indicatorColor="secondary"
        >
          {
            tabs.map((tab) => {
              return (<Tab label={<div>{tab?.name}  <div>{" (" + tab?.employee_count + " Çalışan)"}</div></div>} value={tab?.id} />)
            })
          }
        </Tabs>
      </Box>

      <MUIDataTable
        title={"Personeller"}
        data={data}
        columns={columns}
        options={options}
      />
    </Box>
  )
}

export default TeamPage


const columns = [
  {
    name: "Ad",
    options: {
      filter: true,
      sort: true,
    },
  },
  {
    name: "Takım",
    options: {
      filter: true,
      sort: true,
    },
  },
];