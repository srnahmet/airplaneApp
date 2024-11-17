import { Box, Grid2, Paper, Table, TableHead, TableBody, TableCell, TableContainer, TableRow, Typography } from '@mui/material'
import React, { Fragment, useEffect, useState } from 'react'
import MUIDataTable from "mui-datatables";
import tb2Image from "./../../../assets/images/tb2.png"
import tb3Image from "./../../../assets/images/tb3.png"
import akinciImage from "./../../../assets/images/akinci.png"
import kizileImage from "./../../../assets/images/kizilelma.png"
import { language } from '../../../utils/dataTableOptions';
import { DataGrid } from '@mui/x-data-grid';
import { fetchWithAuth } from '../../../utils/fetchHelper';


const uavTypeToImage = (type) => {
  switch (type) {
    case 1:
      return tb2Image
    case 2:
      return tb3Image
    case 3:
      return akinciImage
    case 4:
      return kizileImage
    default:
      return null;
  }
}

function UAWPage() {

  const [tableData, setTableData] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(false);
  const [selectedRowData, setSelectedRowData] = useState(null);
  const [expandedRowIndex, setExpandedRowIndex] = useState(null);

  // API'den veri çekmek için fonksiyon
  const fetchData = async (start = 0, length = 10, searchValue = null, orderColumn = 0, orderDir = "asc") => {
    setLoading(true);

    const body = {
      "start": start,
      "length": length,
      "order_dir": orderDir
    };

    if (searchValue) body["search_value"] = searchValue;
    if (orderColumn) body["order_column"] = orderColumn;
    try {
      const response = await fetchWithAuth("http://localhost:8000/api/uav-list/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      
      const result = await response;
      setTableData(result.data.map((item) => [
        item.id,
        item.uav_type.name,
        new Date(item.create_date).toLocaleDateString(),
        item.uav_type.id,
      ]));
      setTotalRecords(result.recordsFiltered);
    } catch (error) {
      setTableData(tableData);
      console.error("API hatası:", error);
    } finally {
      setLoading(false);
    }
  };

  // Tablo ayarları
  const options = {
    serverSide: true,
    count: totalRecords,
    rowsPerPage: 10,
    rowsPerPageOptions: [10, 20, 50],
    selectableRows: "none",
    textLabels: language,
    expandableRows: true,
    expandableRowsHeader: false,
    renderExpandableRow: (rowData, rowMeta) => {
      return (
        <tr>
          <td colSpan={1000}>
            <TableContainer component={Paper}>
              <Table >
                <TableHead>
                  <TableRow>
                    <TableCell sx={{color:"6c757d",fontWeight:"bold"}} align="center">Parça</TableCell>
                    <TableCell sx={{color:"6c757d",fontWeight:"bold"}} align="center">Oluşturulma Tarihi</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {selectedRowData?.map((row,index) => (
                    <TableRow
                      key={index}
                    >
                      <TableCell sx={{color:"#6c757d"}} align="center">{row?.part_type_name?.name}</TableCell>
                      <TableCell sx={{color:"#6c757d"}} align="center">{row?.create_date?.split("T")[0]}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </td>
          </tr>
      );
    },
    onTableChange: (action, tableState) => {
      if (action === "changePage" || action === "changeRowsPerPage" || action === "sort" || action === "search") {
        const { page, rowsPerPage, searchText, sortOrder } = tableState;
        const start = page * rowsPerPage;
        const length = rowsPerPage;
        const searchValue = searchText || "";
        const orderColumn = sortOrder ? columns.filter((col) => col.name === sortOrder.name)?.[0]?.column_name : "id";
        const orderDir = sortOrder ? sortOrder?.direction : "asc";
        fetchData(start, length, searchValue, orderColumn, orderDir);
      }
    },
    onRowExpansionChange: (curRowIndex, newExpandedState) => {
      const rowData = tableData[curRowIndex?.[0].index];
      if (newExpandedState) {
        handleRowSelection(rowData);
      }
    },
    customToolbarSelect: () => {
      return null;
    },
  };

  const handleRowSelection = (rowData) => {
    fetch(`http://127.0.0.1:8000/api/parts-list-by-uav-id/${rowData?.[0]}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setSelectedRowData(data)
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      }).finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <MUIDataTable
      title={"IHA Envanteri"}
      data={tableData}
      columns={columns}
      options={options}
    />
  )
}

export default UAWPage


const columns = [
  {
    name: "#",
    column_name: "id",
    options: {
      filter: true,
      sort: true,
    },
  },
  {
    name: "Ad",
    column_name: "uav_type__name",
    options: {
      filter: true,
      sort: true,
    },
  },
  {
    name: "Oluşturulma Tarihi",
    column_name: "create_date",
    options: {
      filter: true,
      sort: true,
    },
  },
  {
    name: "",
    options: {
      filter: false,
      sort: false,
      customBodyRender: (value, tableMeta) => {
        const imageSrc = uavTypeToImage(value);
        return (
          <img
            src={imageSrc}
            alt={`UAV Type ${value}`}
            style={{ width: 100, height: "auto" }}
          />
        );
      },
    },
  },
];