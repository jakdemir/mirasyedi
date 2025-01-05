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
} from '@mui/material';
import { InheritanceResponse } from '../../types';

interface InheritanceResultsProps {
    results: InheritanceResponse;
    familyMembers: Record<string, string>;
}

export const InheritanceResults: React.FC<InheritanceResultsProps> = ({
    results,
    familyMembers,
}) => {
    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat('tr-TR', {
            style: 'currency',
            currency: 'TRY',
        }).format(amount);
    };

    return (
        <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
                Inheritance Distribution Results
            </Typography>
            <Typography variant="subtitle1" gutterBottom>
                Total Distributed: {formatCurrency(results.total_distributed)}
            </Typography>

            <TableContainer component={Paper} sx={{ mt: 2 }}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Heir</TableCell>
                            <TableCell align="right">Share Amount</TableCell>
                            <TableCell align="right">Share Percentage</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {Object.entries(results.shares).map(([id, share]) => (
                            <TableRow key={id}>
                                <TableCell>{familyMembers[id] || 'Unknown'}</TableCell>
                                <TableCell align="right">{formatCurrency(share)}</TableCell>
                                <TableCell align="right">
                                    {((share / results.total_distributed) * 100).toFixed(2)}%
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
}; 