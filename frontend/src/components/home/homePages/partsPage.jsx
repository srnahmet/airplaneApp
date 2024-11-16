import React, { Fragment, useEffect, useState } from 'react'
import { Box, Tab, Tabs, } from '@mui/material'
import { BarChart } from '@mui/x-charts/BarChart';

function PartsPage() {

  // tab
  const [tabValue, setTabValue] = useState(0);
  const [tabs, setTabs] = useState([]);

  const [parts, setParts] = useState([]);
  const [partCounts, setPartCounts] = useState([]);

  const [partTypes, setPartTypes] = useState([]);

  const [loading, setLoading] = useState(false);


  const fetchParthData = (newValue = 0, draftPartyTypes=[]) => {
    setLoading(true)
    fetch(`http://127.0.0.1:8000/api/parts-list-by-uav-type-id-count/${newValue}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const draft = partTypes.length>0 
          ? partTypes.map(item => data.filter(item2 => item2.part_type == item.id)?.[0]?.part_count)
          : draftPartyTypes.map(item => data.filter(item2 => item2.part_type == item.id)?.[0]?.part_count);
        setPartCounts(draft)
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      }).finally(() => setLoading(false));
  }

  const fetchUAVInfo = () => {
    setLoading(true)
    fetch('http://127.0.0.1:8000/api/uav-types/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Hata');
        }
        return response.json();
      })
      .then(data => {
        setTabs(data)
      })
      .catch(error => {
        console.error('Error:', error);
      }).finally(() => setLoading(false));
  }

  const fetchPartTypeInfo = () => {
    setLoading(true)
    fetch('http://127.0.0.1:8000/api/part-types/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Hata');
        }
        return response.json();
      })
      .then(data => {
        setPartTypes(data)
        fetchParthData(0,data);
      })
      .catch(error => {
        console.error('Error:', error);
      }).finally(() => {
        setLoading(false);
      });
  }

  const handleTabValueChange = (event, newValue) => {
    setTabValue(newValue);
    fetchParthData(newValue);
  };

  useEffect(() => {
    fetchUAVInfo();
    fetchPartTypeInfo();
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
          <Tab label={"Tüm Envanter"} value={0} />
          {
            tabs.map((tab) => {
              return (<Tab label={tab?.name} value={tab?.id} />)
            })
          }
        </Tabs>
      </Box>

      <BarChart
        fullWidth
        xAxis={[{ scaleType: 'band', data: partTypes.map(item => item?.name) }]}
        series={[{ data: partCounts }]}
        height={300}
        borderRadius={25}
      />
    </Box>
  )
}

export default PartsPage
