import React, { useState } from 'react';
import {
    Box,
    Stepper,
    Step,
    StepLabel,
    Button,
    Typography,
    Paper,
    StepContent,
} from '@mui/material';
import { FamilyTreeForm } from './FamilyTreeForm';
import { FamilyNode, FamilyTreeFormData } from '../../types';

interface SteppedFamilyFormProps {
    onAddMember: (member: FamilyTreeFormData) => void;
    familyMembers: Record<string, FamilyNode>;
}

export const SteppedFamilyForm: React.FC<SteppedFamilyFormProps> = ({
    onAddMember,
    familyMembers,
}) => {
    const [activeStep, setActiveStep] = useState(0);
    const [hasSpouse, setHasSpouse] = useState<boolean | null>(null);
    const [hasChildren, setHasChildren] = useState<boolean | null>(null);
    const [hasParents, setHasParents] = useState<boolean | null>(null);

    const handleNext = () => {
        setActiveStep((prevStep) => prevStep + 1);
    };

    const handleBack = () => {
        setActiveStep((prevStep) => prevStep - 1);
    };

    const handleAddMember = (member: FamilyTreeFormData) => {
        onAddMember(member);
        if (member.relation === 'spouse') {
            setHasSpouse(true);
            handleNext();
        } else if (member.relation === 'child') {
            setHasChildren(true);
        } else if (member.relation === 'parent') {
            setHasParents(true);
        }
    };

    const hasFirstDegreeHeirs = Boolean(
        Object.values(familyMembers).some(node => 
            node.children.length > 0 || node.person.parent_id
        )
    );

    const steps = [
        {
            label: 'Spouse Information',
            description: 'Add information about the spouse if any.',
            content: (
                <Box>
                    <Typography variant="body1" gutterBottom>
                        Was the deceased person married?
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                        <Button
                            variant={hasSpouse === true ? "contained" : "outlined"}
                            onClick={() => setHasSpouse(true)}
                            sx={{ mr: 1 }}
                        >
                            Yes
                        </Button>
                        <Button
                            variant={hasSpouse === false ? "contained" : "outlined"}
                            onClick={() => {
                                setHasSpouse(false);
                                handleNext();
                            }}
                        >
                            No
                        </Button>
                    </Box>
                    {hasSpouse === true && (
                        <FamilyTreeForm
                            onAddMember={handleAddMember}
                            existingMembers={[]}
                            initialRelation="spouse"
                        />
                    )}
                </Box>
            ),
        },
        {
            label: 'First Degree Heirs',
            description: 'Add children and parents of the deceased.',
            content: (
                <Box>
                    <Typography variant="body1" gutterBottom>
                        Does the deceased have any children or living parents?
                    </Typography>
                    <Box sx={{ mb: 2 }}>
                        <Button
                            variant={hasFirstDegreeHeirs ? "contained" : "outlined"}
                            onClick={() => setHasChildren(true)}
                            sx={{ mr: 1 }}
                        >
                            Yes
                        </Button>
                        <Button
                            variant={hasFirstDegreeHeirs === false ? "contained" : "outlined"}
                            onClick={() => {
                                setHasChildren(false);
                                setHasParents(false);
                                handleNext();
                            }}
                        >
                            No
                        </Button>
                    </Box>
                    {hasFirstDegreeHeirs && (
                        <FamilyTreeForm
                            onAddMember={handleAddMember}
                            existingMembers={Object.entries(familyMembers).map(([id, node]) => ({
                                id,
                                name: node.person.name,
                            }))}
                            allowedRelations={['child', 'parent']}
                        />
                    )}
                </Box>
            ),
        },
    ];

    return (
        <Box sx={{ maxWidth: 600, margin: '0 auto' }}>
            <Stepper activeStep={activeStep} orientation="vertical">
                {steps.map((step, index) => (
                    <Step key={step.label}>
                        <StepLabel>
                            <Typography variant="subtitle1">{step.label}</Typography>
                        </StepLabel>
                        <StepContent>
                            <Typography variant="body2" color="text.secondary" gutterBottom>
                                {step.description}
                            </Typography>
                            {step.content}
                            <Box sx={{ mb: 2 }}>
                                <div>
                                    <Button
                                        disabled={index === 0}
                                        onClick={handleBack}
                                        sx={{ mt: 1, mr: 1 }}
                                    >
                                        Back
                                    </Button>
                                    {(hasSpouse === false || 
                                      (hasSpouse === true && Object.values(familyMembers).some(m => m.person.marriage_info))) &&
                                     index === 0 && (
                                        <Button
                                            variant="contained"
                                            onClick={handleNext}
                                            sx={{ mt: 1, mr: 1 }}
                                        >
                                            Continue
                                        </Button>
                                    )}
                                </div>
                            </Box>
                        </StepContent>
                    </Step>
                ))}
            </Stepper>
        </Box>
    );
}; 