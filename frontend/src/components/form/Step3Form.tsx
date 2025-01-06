import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import {
  Box,
  Button,
  Stack,
  TextField,
  Typography,
  FormControlLabel,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Collapse,
  Divider,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { 
  FormStep1Data, 
  FormStep3Data, 
  RelativeData, 
  RelativeType,
  FirstDegreeData,
  SecondDegreeData,
  ThirdDegreeData
} from '../../types';

interface Step3FormProps {
  degree: 1 | 2 | 3;
  onSubmit: (data: FormStep3Data) => void;
  onBack: () => void;
  onNoHeirs?: () => void;
  defaultValues?: FormStep3Data;
  spouseData?: FormStep1Data;
}

interface AddRelativeFormProps {
  onAdd: (data: { name: string; isAlive: boolean; }) => void;
  type: RelativeType;
}

const AddRelativeForm: React.FC<AddRelativeFormProps> = ({ onAdd, type }) => {
  const [name, setName] = useState('');
  const [isAlive, setIsAlive] = useState(true);

  const handleAdd = () => {
    if (name.trim()) {
      onAdd({ name, isAlive });
      setName('');
      setIsAlive(true);
    }
  };

  return (
    <Stack spacing={2} sx={{ mt: 2, mb: 2 }}>
      <TextField
        label={`${type.charAt(0).toUpperCase() + type.slice(1)} Name`}
        value={name}
        onChange={(e) => setName(e.target.value)}
        fullWidth
        autoFocus
      />
      <FormControlLabel
        control={
          <Switch
            checked={isAlive}
            onChange={(e) => setIsAlive(e.target.checked)}
          />
        }
        label="Alive"
      />
      <Button
        onClick={handleAdd}
        variant="contained"
        disabled={!name.trim()}
        fullWidth
      >
        Add {type.charAt(0).toUpperCase() + type.slice(1)}
      </Button>
    </Stack>
  );
};

const FirstDegreeForm: React.FC<{
  data: FirstDegreeData;
  onChange: (data: FirstDegreeData) => void;
}> = ({ data, onChange }) => {
  const [isAddingChild, setIsAddingChild] = useState(false);

  const handleAddChild = ({ name, isAlive }: { name: string; isAlive: boolean }) => {
    onChange({
      children: [
        ...data.children,
        {
          id: `child-${Date.now()}`,
          name,
          is_alive: isAlive,
          type: RelativeType.CHILD,
        },
      ],
    });
    setIsAddingChild(false);
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Add Children
      </Typography>
      
      <Button
        startIcon={<AddIcon />}
        onClick={() => setIsAddingChild(!isAddingChild)}
        variant="outlined"
        color="primary"
        sx={{ mb: 2 }}
      >
        {isAddingChild ? 'Cancel' : 'Add Child'}
      </Button>

      <Collapse in={isAddingChild}>
        <AddRelativeForm onAdd={handleAddChild} type={RelativeType.CHILD} />
      </Collapse>

      <FamilyTreeTable relatives={data.children} />
    </Box>
  );
};

const SecondDegreeForm: React.FC<{
  data: SecondDegreeData;
  onChange: (data: SecondDegreeData) => void;
}> = ({ data, onChange }) => {
  const [isAddingParent, setIsAddingParent] = useState<'mother' | 'father' | null>(null);
  const [isAddingSibling, setIsAddingSibling] = useState(false);

  const handleAddParent = (type: 'mother' | 'father') => ({ name, isAlive }: { name: string; isAlive: boolean }) => {
    onChange({
      ...data,
      [type]: {
        id: `${type}-${Date.now()}`,
        name,
        is_alive: isAlive,
        type: RelativeType.PARENT,
      },
    });
    setIsAddingParent(null);
  };

  const handleAddSibling = ({ name, isAlive }: { name: string; isAlive: boolean }) => {
    onChange({
      ...data,
      siblings: [
        ...data.siblings,
        {
          id: `sibling-${Date.now()}`,
          name,
          is_alive: isAlive,
          type: RelativeType.CHILD,
          parent_id: data.father?.id || data.mother?.id,
        },
      ],
    });
    setIsAddingSibling(false);
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Add Parents
      </Typography>
      
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        {!data.mother && (
          <Button
            startIcon={<AddIcon />}
            onClick={() => setIsAddingParent('mother')}
            variant="outlined"
          >
            Add Mother
          </Button>
        )}
        {!data.father && (
          <Button
            startIcon={<AddIcon />}
            onClick={() => setIsAddingParent('father')}
            variant="outlined"
          >
            Add Father
          </Button>
        )}
      </Stack>

      <Collapse in={!!isAddingParent}>
        <AddRelativeForm 
          onAdd={handleAddParent(isAddingParent as 'mother' | 'father')} 
          type={RelativeType.PARENT} 
        />
      </Collapse>

      {(data.mother || data.father) && (
        <>
          <Divider sx={{ my: 2 }} />
          <Typography variant="h6" gutterBottom>
            Add Siblings
          </Typography>
          
          <Button
            startIcon={<AddIcon />}
            onClick={() => setIsAddingSibling(!isAddingSibling)}
            variant="outlined"
            sx={{ mb: 2 }}
          >
            {isAddingSibling ? 'Cancel' : 'Add Sibling'}
          </Button>

          <Collapse in={isAddingSibling}>
            <AddRelativeForm onAdd={handleAddSibling} type={RelativeType.CHILD} />
          </Collapse>
        </>
      )}

      <FamilyTreeTable 
        relatives={[
          ...(data.mother ? [data.mother] : []),
          ...(data.father ? [data.father] : []),
          ...data.siblings,
        ]} 
      />
    </Box>
  );
};

const ThirdDegreeForm: React.FC<{
  data: ThirdDegreeData;
  onChange: (data: ThirdDegreeData) => void;
}> = ({ data, onChange }) => {
  const [addingRelative, setAddingRelative] = useState<{
    side: 'maternal' | 'paternal';
    type: 'grandmother' | 'grandfather' | 'uncle';
  } | null>(null);

  const handleAddRelative = (
    side: 'maternal' | 'paternal',
    type: 'grandmother' | 'grandfather' | 'uncle'
  ) => ({ name, isAlive }: { name: string; isAlive: boolean }) => {
    const newData = { ...data };
    if (type === 'uncle') {
      newData[side].uncles.push({
        id: `uncle-${side}-${Date.now()}`,
        name,
        is_alive: isAlive,
        type: RelativeType.CHILD,
        parent_id: newData[side].grandfather?.id,
      });
    } else {
      newData[side][type] = {
        id: `${type}-${side}-${Date.now()}`,
        name,
        is_alive: isAlive,
        type: RelativeType.GRANDPARENT,
      };
    }
    onChange(newData);
    setAddingRelative(null);
  };

  const renderSide = (side: 'maternal' | 'paternal') => (
    <Box sx={{ mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        {side.charAt(0).toUpperCase() + side.slice(1)} Side
      </Typography>
      
      <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
        {!data[side].grandmother && (
          <Button
            startIcon={<AddIcon />}
            onClick={() => setAddingRelative({ side, type: 'grandmother' })}
            variant="outlined"
          >
            Add Grandmother
          </Button>
        )}
        {!data[side].grandfather && (
          <Button
            startIcon={<AddIcon />}
            onClick={() => setAddingRelative({ side, type: 'grandfather' })}
            variant="outlined"
          >
            Add Grandfather
          </Button>
        )}
        {(data[side].grandmother || data[side].grandfather) && (
          <Button
            startIcon={<AddIcon />}
            onClick={() => setAddingRelative({ side, type: 'uncle' })}
            variant="outlined"
          >
            Add Uncle/Aunt
          </Button>
        )}
      </Stack>

      <Collapse in={addingRelative?.side === side}>
        <AddRelativeForm 
          onAdd={handleAddRelative(side, addingRelative?.type as any)} 
          type={addingRelative?.type === 'uncle' ? RelativeType.CHILD : RelativeType.GRANDPARENT} 
        />
      </Collapse>

      <FamilyTreeTable 
        relatives={[
          ...(data[side].grandmother ? [data[side].grandmother] : []),
          ...(data[side].grandfather ? [data[side].grandfather] : []),
          ...data[side].uncles,
        ]} 
      />
    </Box>
  );

  return (
    <Box>
      {renderSide('maternal')}
      <Divider sx={{ my: 3 }} />
      {renderSide('paternal')}
    </Box>
  );
};

const FamilyTreeTable: React.FC<{
  relatives: RelativeData[];
}> = ({ relatives }) => {
  return (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Relationship</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {relatives.length === 0 ? (
            <TableRow>
              <TableCell colSpan={3} align="center">
                No relatives added
              </TableCell>
            </TableRow>
          ) : (
            relatives.map((relative) => (
              <TableRow key={relative.id}>
                <TableCell>{relative.name}</TableCell>
                <TableCell>{relative.type}</TableCell>
                <TableCell>{relative.is_alive ? 'Alive' : 'Deceased'}</TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

const Step3Form: React.FC<Step3FormProps> = ({
  degree,
  onSubmit,
  onBack,
  onNoHeirs,
  defaultValues,
  spouseData,
}) => {
  const { handleSubmit, setValue, watch } = useForm<FormStep3Data>({
    defaultValues: defaultValues || {
      degree,
      firstDegree: { children: [] },
      secondDegree: { siblings: [] },
      thirdDegree: { maternal: { uncles: [] }, paternal: { uncles: [] } },
    },
  });

  const formData = watch();

  const handleFormSubmit = (data: FormStep3Data) => {
    onSubmit({
      ...data,
      degree,
    });
  };

  const renderDegreeForm = () => {
    switch (degree) {
      case 1:
        return (
          <FirstDegreeForm
            data={formData.firstDegree!}
            onChange={(data) => setValue('firstDegree', data)}
          />
        );
      case 2:
        return (
          <SecondDegreeForm
            data={formData.secondDegree!}
            onChange={(data) => setValue('secondDegree', data)}
          />
        );
      case 3:
        return (
          <ThirdDegreeForm
            data={formData.thirdDegree!}
            onChange={(data) => setValue('thirdDegree', data)}
          />
        );
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit(handleFormSubmit)} sx={{ maxWidth: 800, mx: 'auto', p: 2 }}>
      {spouseData?.has_spouse && (
        <Box sx={{ mb: 3 }}>
      <Typography variant="h6" gutterBottom>
            Spouse Information
      </Typography>
      <FamilyTreeTable
            relatives={[
              {
                id: 'spouse',
                name: spouseData.spouse_name!,
                is_alive: spouseData.spouse_is_alive,
                type: RelativeType.SPOUSE,
              },
            ]}
          />
        </Box>
      )}

      {renderDegreeForm()}

      <Stack direction="row" spacing={2} sx={{ mt: 4 }}>
        <Button variant="outlined" onClick={onBack} fullWidth>
          Back
        </Button>
        {onNoHeirs && (
          <Button variant="outlined" onClick={onNoHeirs} fullWidth color="secondary">
            No {degree === 1 ? 'Children' : degree === 2 ? 'Parents' : 'Grandparents'}
          </Button>
        )}
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
        >
          Calculate Inheritance
        </Button>
      </Stack>
    </Box>
  );
};

export default Step3Form; 