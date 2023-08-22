import { ModalTitle } from '../../util/modal-title';
import {
  Box,
  Button,
  IconButton,
  Stack,
  Tooltip,
  Typography
} from '@mui/material';
import * as React from 'react';
import { Lecture } from '../../../model/lecture';
import { Assignment } from '../../../model/assignment';
import { Submission } from '../../../model/submission';
import {
  getProperties,
  updateSubmission
} from '../../../services/submissions.service';
import { GradeBook } from '../../../services/gradebook';
import { createManualFeedback } from '../../../services/grading.service';
import { FilesList } from '../../util/file-list';
import { AgreeDialog } from '../../util/dialog';
import ReplayIcon from '@mui/icons-material/Replay';
import { enqueueSnackbar } from 'notistack';
import { openBrowser } from '../overview/util';
import { LoadingButton } from '@mui/lab';

export interface IManualGradingProps {
  lecture: Lecture;
  assignment: Assignment;
  submission: Submission;
  username: string;
  onClose: () => void;
}

export const ManualGrading = (props: IManualGradingProps) => {
  const [gradeBook, setGradeBook] = React.useState(null);

  const [path, setPath] = React.useState(
    `manualgrade/${props.lecture.code}/${props.assignment.id}/${props.submission.id}`
  );

  const [showDialog, setShowDialog] = React.useState(false);
  const [loading, setLoading] = React.useState(false);
  const [dialogContent, setDialogContent] = React.useState({
    title: '',
    message: '',
    handleAgree: null,
    handleDisagree: null
  });

  React.useEffect(() => {
    reloadProperties();
  },[]);

  const openFinishDialog = () => {
    setDialogContent({
      title: 'Confirm Grading',
      message: 'Do you want to save the assignment grading?',
      handleAgree: finishGrading,
      handleDisagree: () => {
        setShowDialog(false);
      }
    });
    setShowDialog(true);
  };

  const finishGrading = () => {
    props.submission.manual_status = 'manually_graded';
    updateSubmission(
      props.lecture.id,
      props.assignment.id,
      props.submission.id,
      props.submission
    ).then(
      response => {
        props.onClose();
        enqueueSnackbar('Successfully Graded Submission', {
          variant: 'success'
        });
      },
      err => {
        enqueueSnackbar(err.message, {
          variant: 'error'
        });
      }
    );
  };

  const reloadProperties = () => {
    getProperties(
      props.lecture.id,
      props.assignment.id,
      props.submission.id
    ).then(properties => {
      const gradeBook = new GradeBook(properties);
      setGradeBook(gradeBook);
    });
  };
  
  const handlePullSubmission = async () => {
    await createManualFeedback(props.lecture.id, props.assignment.id, props.submission.id).then(
      response => {
        openBrowser(path);
        enqueueSnackbar('Successfully Pulled Submission', {
          variant: 'success'
        });
      },
      err => {
        enqueueSnackbar(err.message, {
          variant: 'error'
        });
      }
    );
  };

  return (
    <Box sx={{ overflow: 'scroll', height: '100%' }}>
      <ModalTitle title={'Manual Grading ' + props.assignment.id} />
      <Box sx={{ m: 2, mt: 5 }}>
        <Stack direction="row" spacing={2} sx={{ ml: 2 }}>
          <Stack sx={{ mt: 0.5 }}>
            <Typography
              textAlign="right"
              color="text.secondary"
              sx={{ fontSize: 12, height: 35 }}
            >
              Username
            </Typography>
            <Typography
              textAlign="right"
              color="text.secondary"
              sx={{ fontSize: 12, height: 35 }}
            >
              Lecture
            </Typography>
            <Typography
              textAlign="right"
              color="text.secondary"
              sx={{ fontSize: 12, height: 35 }}
            >
              Assignment
            </Typography>
            <Typography
              textAlign="right"
              color="text.secondary"
              sx={{ fontSize: 12, height: 35 }}
            >
              Points
            </Typography>
            <Typography
              textAlign="right"
              color="text.secondary"
              sx={{ fontSize: 12, height: 35 }}
            >
              Extra Credit
            </Typography>
          </Stack>
          <Stack>
            <Typography
              color="text.primary"
              sx={{ display: 'inline-block', fontSize: 16, height: 35 }}
            >
              {props.username}
            </Typography>
            <Typography
              color="text.primary"
              sx={{ display: 'inline-block', fontSize: 16, height: 35 }}
            >
              {props.lecture.name}
            </Typography>
            <Typography
              color="text.primary"
              sx={{ display: 'inline-block', fontSize: 16, height: 35 }}
            >
              {props.assignment.name}
              <Typography
                color="text.secondary"
                sx={{
                  display: 'inline-block',
                  fontSize: 14,
                  ml: 2,
                  height: 35
                }}
              >
                {props.assignment.type}
              </Typography>
            </Typography>
            <Typography
              color="text.primary"
              sx={{ display: 'inline-block', fontSize: 16, height: 35 }}
            >
              {gradeBook?.getPoints()}
              <Typography
                color="text.secondary"
                sx={{ display: 'inline-block', fontSize: 14, ml: 0.25 }}
              >
                /{gradeBook?.getMaxPoints()}
              </Typography>
            </Typography>
            <Typography
              color="text.primary"
              sx={{ display: 'inline-block', fontSize: 16, height: 35 }}
            >
              {gradeBook?.getExtraCredits()}
            </Typography>
          </Stack>
        </Stack>
      </Box>
      <Typography sx={{ m: 2, mb: 0 }}>Submission Files</Typography>
      <Box sx={{ overflowY: 'auto' }}>
        <FilesList path={path} sx={{ m: 2 }} />
      </Box>

      <Stack direction={'row'} sx={{ ml: 2 }} spacing={2}>
        <Tooltip title="Reload">
          <IconButton aria-label="reload" onClick={() => reloadProperties()}>
            <ReplayIcon />
          </IconButton>
        </Tooltip>

        <LoadingButton
          loading={loading}
          color="primary"
          variant="outlined"
          onClick={async () => {
            setLoading(true);
            await handlePullSubmission();
            setLoading(false);
          }}
        >
          Pull Submission
        </LoadingButton>

        <Button
          variant="outlined"
          color="success"
          onClick={openFinishDialog}
          sx={{ ml: 2 }}
        >
          Finish Manual Grading
        </Button>
      </Stack>

      <AgreeDialog open={showDialog} {...dialogContent} />
    </Box>
  );
}