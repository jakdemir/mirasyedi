import { useState } from 'react';
import {
    Container,
    Box,
    Typography,
    TextField,
    Button,
    Paper,
    Grid,
    Alert,
} from '@mui/material';
import { SteppedFamilyForm } from './components/family-tree/SteppedFamilyForm';
import { InheritanceResults } from './components/inheritance/InheritanceResults';
import { calculateInheritance } from './services/api';
import { FamilyNode, FamilyTreeFormData, InheritanceResponse } from './types';
import { v4 as uuidv4 } from 'uuid';

function App() {
    const [estateValue, setEstateValue] = useState<number>(0);
    const [familyMembers, setFamilyMembers] = useState<Record<string, FamilyNode>>({});
    const [inheritanceResults, setInheritanceResults] = useState<InheritanceResponse | null>(
        null
    );
    const [error, setError] = useState<string | null>(null);

    const handleAddMember = (formData: FamilyTreeFormData) => {
        const id = uuidv4();
        const newMember: FamilyNode = {
            person: {
                id,
                name: formData.name,
                is_alive: formData.is_alive,
                share: 0,
            },
            children: [],
        };

        if (formData.relation === 'spouse') {
            newMember.person.marriage_info = {
                marriage_order: formData.marriage_order || 1,
                is_current: formData.is_current_marriage || true,
            };
        }

        setFamilyMembers((prev) => {
            const updated = { ...prev };
            if (formData.relation === 'child' && formData.parent_id) {
                const parent = updated[formData.parent_id];
                if (parent) {
                    newMember.person.parent_id = formData.parent_id;
                    parent.children.push(newMember);
                }
            } else {
                updated[id] = newMember;
            }
            return updated;
        });
    };

    const handleCalculate = async () => {
        try {
            setError(null);
            if (estateValue <= 0) {
                setError('Estate value must be greater than 0');
                return;
            }

            if (Object.keys(familyMembers).length === 0) {
                setError('Please add at least one family member');
                return;
            }

            const rootNode = Object.values(familyMembers)[0];
            const response = await calculateInheritance({
                estate_value: estateValue,
                family_tree: rootNode,
            });
            setInheritanceResults(response);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        }
    };

    const getMemberNames = () => {
        return Object.fromEntries(
            Object.entries(familyMembers).map(([id, node]) => [id, node.person.name])
        );
    };

    return (
        <Container maxWidth="lg">
            <Box sx={{ my: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom align="center">
                    Turkish Inheritance Calculator
                </Typography>

                <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2 }}>
                            <Typography variant="h6" gutterBottom>
                                Estate Information
                            </Typography>
                            <TextField
                                fullWidth
                                type="number"
                                label="Estate Value (TRY)"
                                value={estateValue}
                                onChange={(e) => setEstateValue(Number(e.target.value))}
                                margin="normal"
                            />
                            <SteppedFamilyForm
                                onAddMember={handleAddMember}
                                familyMembers={familyMembers}
                            />
                            {Object.keys(familyMembers).length > 0 && (
                                <Button
                                    variant="contained"
                                    color="primary"
                                    onClick={handleCalculate}
                                    fullWidth
                                    sx={{ mt: 2 }}
                                >
                                    Calculate Inheritance
                                </Button>
                            )}
                        </Paper>
                    </Grid>

                    <Grid item xs={12} md={6}>
                        {error && (
                            <Alert severity="error" sx={{ mb: 2 }}>
                                {error}
                            </Alert>
                        )}
                        {inheritanceResults && (
                            <Paper sx={{ p: 2 }}>
                                <InheritanceResults
                                    results={inheritanceResults}
                                    familyMembers={getMemberNames()}
                                />
                            </Paper>
                        )}
                    </Grid>
                </Grid>
            </Box>
        </Container>
    );
}

export default App;
