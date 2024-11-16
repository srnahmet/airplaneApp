import { Box, Grid2, Typography } from '@mui/material'
import React, { Fragment, useEffect, useState } from 'react'
import MUIDataTable from "mui-datatables";
import tb2Image from "./../../../assets/images/tb2.png"
import tb3Image from "./../../../assets/images/tb3.png"
import akinciImage from "./../../../assets/images/akinci.png"
import kizileImage from "./../../../assets/images/kizilelma.png"
import { language } from '../../../utils/dataTableOptions';

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

  const [data, setData] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [loading, setLoading] = useState(false);

  // API'den veri çekmek için fonksiyon
  const fetchData = async (start = 0, length = 10, searchValue = null, orderColumn = 0, orderDir = "asc") => {
    setLoading(true);

    const body = {
      "start":start,
      "length":length,
      "order_dir":orderDir
    };

    if (searchValue) body["search_value"] = searchValue;
    if (orderColumn) body["order_column"] = orderColumn;
    try {
      const response = await fetch("http://localhost:8000/api/uav-list/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        throw new Error("Veri çekilirken bir hata oluştu!");
      }

      const result = await response.json();
      setData(result.data.map((item) => [
        item.uav_type.name,
        new Date(item.create_date).toLocaleDateString(),
        item.uav_type.id,
      ]));
      setTotalRecords(result.recordsTotal);
    } catch (error) {
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
    textLabels:language,
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
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <MUIDataTable
      title={"IHA Envanteri"}
      data={data}
      columns={columns}
      options={options}
    />
  )
}

export default UAWPage


const columns = [
  {
    name: "Ad",
    column_name:"uav_type__name",
    options: {
      filter: true,
      sort: true,
    },
  },
  {
    name: "Oluşturulma Tarihi",
    column_name:"create_date",
    options: {
      filter: true,
      sort: true,
    },
  },
  {
    name: "#",
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