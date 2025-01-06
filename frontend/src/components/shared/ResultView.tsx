import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Grid,
} from '@mui/material';
import { InheritanceResponse } from '../../types';
import FamilyTreeView from './FamilyTreeView';

interface ResultViewProps {
  result: InheritanceResponse;
  onReset: () => void;
}

const ResultView: React.FC<ResultViewProps> = ({ result, onReset }) => {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('tr-TR', {
      style: 'currency',
      currency: 'TRY',
    }).format(amount);
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 2 }}>
      <Typography variant="h5" gutterBottom>
        Inheritance Distribution Results
      </Typography>

      <Paper sx={{ mb: 3, p: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          Total Distributed Amount: {formatCurrency(result.total_distributed)}
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <FamilyTreeView familyTree={result.family_tree} type="deceased" />
        </Grid>
        <Grid item xs={12} md={6}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Relation</TableCell>
                  <TableCell align="right">Share Amount</TableCell>
                  <TableCell align="right">Share Percentage</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {Object.entries(result.summary).map(([id, share]) => (
                  <TableRow key={id}>
                    <TableCell>{share.name}</TableCell>
                    <TableCell>{share.relation}</TableCell>
                    <TableCell align="right">{formatCurrency(share.share)}</TableCell>
                    <TableCell align="right">
                      {share.share_percentage.toFixed(2)}%
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4, textAlign: 'center' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={onReset}
          size="large"
        >
          Calculate Another Inheritance
        </Button>
      </Box>
    </Box>
  );
};

export default ResultView; 