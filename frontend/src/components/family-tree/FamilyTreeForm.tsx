import React, { useState, useEffect } from 'react';
import {
    Box,
    TextField,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Switch,
    FormControlLabel,
    Button,
    Typography,
    SelectChangeEvent,
} from '@mui/material';
import { FamilyTreeFormData } from '../../types';

interface FamilyTreeFormProps {
    onAddMember: (member: FamilyTreeFormData) => void;
    existingMembers: { id: string; name: string }[];
    initialRelation?: 'spouse' | 'child' | 'parent' | null;
    allowedRelations?: ('spouse' | 'child' | 'parent')[];
}

export const FamilyTreeForm: React.FC<FamilyTreeFormProps> = ({
    onAddMember,
    existingMembers,
    initialRelation = null,
    allowedRelations = ['spouse', 'child', 'parent'],
}) => {
    const [formData, setFormData] = useState<FamilyTreeFormData>({
        name: '',
        is_alive: true,
        relation: initialRelation,
        parent_id: undefined,
        marriage_order: 1,
        is_current_marriage: true,
    });

    useEffect(() => {
        if (initialRelation) {
            setFormData(prev => ({ ...prev, relation: initialRelation }));
        }
    }, [initialRelation]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onAddMember(formData);
        setFormData({
            name: '',
            is_alive: true,
            relation: initialRelation,
            parent_id: undefined,
            marriage_order: 1,
            is_current_marriage: true,
        });
    };

    const handleTextChange = (field: keyof FamilyTreeFormData) => (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        setFormData((prev) => ({
            ...prev,
            [field]: e.target.value,
        }));
    };

    const handleSelectChange = (field: keyof FamilyTreeFormData) => (
        e: SelectChangeEvent
    ) => {
        setFormData((prev) => ({
            ...prev,
            [field]: e.target.value,
        }));
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
                Add Family Member
            </Typography>

            <TextField
                fullWidth
                label="Name"
                value={formData.name}
                onChange={handleTextChange('name')}
                margin="normal"
                required
            />

            <FormControlLabel
                control={
                    <Switch
                        checked={formData.is_alive}
                        onChange={(e) =>
                            setFormData((prev) => ({ ...prev, is_alive: e.target.checked }))
                        }
                    />
                }
                label="Is Alive"
            />

            {!initialRelation && (
                <FormControl fullWidth margin="normal">
                    <InputLabel>Relation</InputLabel>
                    <Select
                        value={formData.relation || ''}
                        onChange={handleSelectChange('relation')}
                        required
                    >
                        {allowedRelations.map(relation => (
                            <MenuItem key={relation} value={relation}>
                                {relation.charAt(0).toUpperCase() + relation.slice(1)}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            )}

            {formData.relation === 'child' && existingMembers.length > 0 && (
                <FormControl fullWidth margin="normal">
                    <InputLabel>Parent</InputLabel>
                    <Select
                        value={formData.parent_id || ''}
                        onChange={handleSelectChange('parent_id')}
                        required
                    >
                        {existingMembers.map((member) => (
                            <MenuItem key={member.id} value={member.id}>
                                {member.name}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
            )}

            {formData.relation === 'spouse' && (
                <>
                    <TextField
                        fullWidth
                        type="number"
                        label="Marriage Order"
                        value={formData.marriage_order}
                        onChange={handleTextChange('marriage_order')}
                        margin="normal"
                        required
                    />
                    <FormControlLabel
                        control={
                            <Switch
                                checked={formData.is_current_marriage}
                                onChange={(e) =>
                                    setFormData((prev) => ({
                                        ...prev,
                                        is_current_marriage: e.target.checked,
                                    }))
                                }
                            />
                        }
                        label="Current Marriage"
                    />
                </>
            )}

            <Button
                type="submit"
                variant="contained"
                color="primary"
                sx={{ mt: 2 }}
                fullWidth
            >
                Add Member
            </Button>
        </Box>
    );
}; 